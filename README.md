xBrowse: Laptop Edition
=======================

This repo provides a quick installer for developers to begin contributing to [xBrowse](https://atgu.mgh.harvard.edu/xbrowse). 
Deploying an xBrowse instance in the wild is pretty involved, 
so this repository provides a "getting started" deployment with minimal configuration, smaller reference datasets, etc. 

Note that this installation should **not** be used to deploy xBrowse in production. xBrowse is still in *beta*, and we aren't ready to endorse it for external use yet. (Hopefully soon!)

## How It Works 

This repository provides code for installing up a lightweight instance 
on your laptop, within a Vagrant virtual machine. 

xBrowse is run entirely in this virtual machine - the "guest" machine - 
but you can visit this version of the xBrowse website on your laptop's web browser. 

The xBrowse application code is mounted on a "shared" directory - meaning it is accessible by both your laptop and the VM. 
So, you follow the standard development workflow: edit the code, refresh your browser, and check out the changes. 
However, no code is actually executed on your laptop - it all happens within the VM. 


## Preparing 

The only prerequisite is that you have [Vagrant](http://vagrantup.com) installed. 
Installation is pretty straightforward on Mac. Make sure the vagrant command line utility is on your PATH: 

	$ vagrant -v
	Vagrant 1.6.3

After Vagrant is installed, clone this repository: 

	git clone https://github.com/xbrowse/xbrowse-laptop.git
	cd xbrowse-laptop

From now on, consider `xbrowse-laptop` the working directory for this installation - it will be mounted to the VM as a shared directory.  

Before you build anything, you also need to download a couple other resources to this working directory.
First, clone the xBrowse repository: 

	 git clone https://github.com/xbrowse/xbrowse.git

Next, download and extract a tarball with some resource data needed for this deployment. 
(It's 3.8GB, so may take a while...)

	wget ftp://atguftp.mgh.harvard.edu/xbrowse-laptop-downloads.tar.gz
	tar -xzf xbrowse-laptop-downloads.tar.gz

Finally, there is one resource that is not included in that tarball - the ExAC Allele Frequencies. 
Download that too: 

	wget ftp://ftp.broadinstitute.org/pub/ExAC_release/release0.2/ExAC.r0.2.sites.vep.vcf.gz

At this point, make sure the xbrowse-laptop directory (the same one with this README.md file) should 
have the directories `xbrowse` and `xbrowse-laptop-downloads`, and one file `ExAC.r0.2.sites.vep.vcf.gz`. 
(Many of the file paths within the VM are hardcoded.) 

## Provisioning the machine 

Now it's time to create the actual VM. 
Run the following command (this will take ~30 minutes): 

	vagrant up

This provisions a base Ubuntu box (14.04). If curious, you can check out the steps in `bootstrap.sh`. 

## Setting up xBrowse

The VM is now set up to run xBrowse, but the xBrowse instance has not been set up yet. We'll do that now. 

First, log in to the VM: 

	vagrant ssh

This is analogous to logging in to a remote web server, but it's actually on your laptop. 
Once you're logged in, run the following command: 

	./manage.py syncdb --all

This is a Django command that creates the database xBrowse uses to store users and other website data. 
It will ask you to create a username and password for the "superuser" - this is just stored locally, it can be anything. 

`syncdb` doesn't create any of the actual scientific resources. We need to run another command for that: 

	./manage.py load_resources

This will take ~20 minutes. (Note that there are multiple progress bars in sequence.)

xBrowse is now fully installed. You can visit http://localhost:8000 on your web browser and log in with the username you just created. 

## Loading data

That's it - xBrowse is all set up! 
However, you'll want to actually load some data. For that, pick up at the instructions in the main xbrowse repository: https://github.com/xbrowse/xbrowse#add-a-project

