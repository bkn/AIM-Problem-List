# -*- coding: utf-8 -

from couchdbkit.ext.django.loading import get_db
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete

from aimpl_proxy.aimpl.utils import popen3


def delete_pl(sender, instance=None, **kwargs):
    """
    callback to signal "pre-delete",
    delete records in couuchdb. 
    
    Note: Obviously a way to chain views on CouchDB 
    side would be better but waiting that just get 
    results using _all_docs and do bulk delete at
    the end.
    """
    db = get_db('aimpl')
    docs = []
    # get all revisions of this pl
    for row in db.all_docs(startkey=instance.path, include_docs=True):
        docs.append(row['doc'])
        # get all sections
        sections = db.all_docs(keys=row['doc']['section_ids'], include_docs=True)
        for sec in sections:
            docs.append(sec["doc"])
            # get all pb blocks
            pblocks = db.all_docs(keys=sec["doc"]["pblock_ids"], include_docs=True)
            for block in pblocks:
                docs.append(block["doc"])
        # get all web remarks
        remarks = db.view("aimpl/web_remarks")
        for remark in remarks:
            docs.append(remark['value'])
    
    db.bulk_delete(docs,  all_or_nothing=True)
    
    
class ProblemList(models.Model):
    name = models.CharField(max_length=1024)
    path = models.SlugField()
    editors = models.ManyToManyField(User)
    latex = models.FileField(upload_to="latex/")
    

    def __unicode__(self):
        return self.name
        
    def save(self, **kwargs):
        super(ProblemList, self).save(**kwargs)
        cmd = "%s %s" %  (settings.LATEX_TO_JSON_CMD,str(self.latex.path))
        stdin, stdout, stderr = popen3(cmd)
        err = stderr.read()
        if err:
            raise ValueError(err)        
        
post_delete.connect(delete_pl, sender=ProblemList)            

class Section(models.Model):
    pl = models.ForeignKey(ProblemList)
    title = models.CharField(max_length=1024)

    def __unicode__(self):
        return self.title

class Block(models.Model):
    section = models.ForeignKey(Section)
    content = models.TextField()

    def __unicode__(self):
        return self.content

class Remark(models.Model):
    block = models.ForeignKey(Block)
    created = models.DateTimeField(default=datetime.now)
    content = models.TextField()
    is_approved = models.BooleanField(default=False)

    def __unicode__(self):
        return self.content

