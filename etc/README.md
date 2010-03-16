Include proxy.conf into your Apache httpd configuration. For example, like this:

    Include /path/to/proxy.conf

It requires `mod_proxy` and `mod_rewrite` to be loaded. Please refer to the
Apache httpd documentation for how to do that.

In addition, add this line to your `/etc/hosts` file:

    127.0.0.1 aimpl.org

Now point your browser at http://aimpl.org/pl/problemlistname