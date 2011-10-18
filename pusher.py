#def run_unit_tests(pusher):
#    codir = pusher.checkout_dir()
#    (out,err) = pusher.execute("pushd %s && nosetests && popd" % codir)
#    return ("OK" in err,out,err)

def post_rsync(pusher):
    """ need to restart apache2 """
    (out,err) = pusher.execute(["ssh","monty.ccnmtl.columbia.edu","/var/www/twister/init.sh","/var/www/twister/"])
    (out2,err2) = pusher.execute(["ssh","monty.ccnmtl.columbia.edu","/bin/ln","-s","/usr/lib/python2.5/site-packages/ldap","/var/www/twister/working-env/lib/python2.5/"])
    (out3,err3) = pusher.execute(["ssh","monty.ccnmtl.columbia.edu","/bin/ln","-s","/usr/lib/python2.5/site-packages/_ldap.so","/var/www/twister/working-env/lib/python2.5/"])        
    (out4,err4) = pusher.execute(["ssh","monty.ccnmtl.columbia.edu","sudo","/usr/bin/supervisorctl","restart","twister"])
    out += out2 + out3 + out4
    err += err2 + err3 + err4
    return (True,out,err)  
