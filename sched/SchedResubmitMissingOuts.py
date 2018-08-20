#!/usr/bin/python

from glob import glob
import subprocess

#_____________________________________________________________________________
def resubmit(missing_list):

    #resubmit jobs with missing outputs

    print "Resubmitting the missing jobs"

    for job in missing_list:
        session_num = job.split("_")
        #resubmit command
        cmd = "star-submit -r " + session_num[1] + " " + session_num[0] + ".session.xml"
        p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = p.communicate()
        print out[0]
        print out[1]

#_____________________________________________________________________________
def search_in_prod(basedir, prod_name):

    basedir = basedir + "/" + prod_name

    #get list of jobs
    cmd = basedir + "/sched/*_*.csh"
    joblist = []
    for job in glob(cmd):
        joblist.append(job.split("sched/sched")[1].split(".csh")[0])

    #get list of outputs
    cmd = basedir + "/*.root"
    outlist = []
    for out in glob(cmd):
        outlist.append(out.split("/"+prod_name+"/")[1].split(".root")[0])

    missing_list = []
    for job in joblist:
        if job not in outlist:
            missing_list.append(job)

    if len(missing_list) == 0: return

    #missing jobs were found
    print "Missing outputs in'", prod_name, "':"
    for job in missing_list:
        print job

    resubmit(missing_list)

#_____________________________________________________________________________
if __name__ == "__main__":

    basedir = "/gpfs01/star/pwg/jaroslav/star-upc/trees/muDst/muDst_run1a"

    #production names
    plist=["prod", "low", "mid", "high"]

    for prod_name in plist:
        search_in_prod(basedir, prod_name)





