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

	git clone https://github.com/xbrowse/xbrowse-laptop
	cd xbrowse-laptop

From now on, consider `xbrowse-laptop` the working directory for this installation. 
It will be mounted to the VM as a shared directory, and many of the file paths are hardcoded. 

Before you build anything, you need to download a couple other resources to this working directory. 

download and extract a tarball of all the data needed for this deployment. 
(It's 3.8GB, so may take a while...)

	wget ftp://atguftp.mgh.harvard.edu/xbrowse-laptop-downloads.tar.gz
	tar -xzf xbrowse-laptop-downloads.tar.gz

Now it's time to initialize the VM (this will take ~30 minutes). 
Run the following command: 

	vagrant up

This command does the following: 

- Creates a virtual machine that can run xBrowse

- Provisions the machine with required packages

- Downloads the xBrowse source code into a shared directory

- Initializes the machine as a "valid" xbrowse instance. 

If curious, all of these steps are contained in `bootstrap.sh`. 
(Indeed, we'll need a much better way to organize these steps, but this was easiest for now.)

## Provisioning the machine 

## Setting up xBrowse

### Running xBrowse

When `vagrant up` finishes, visit `http://localhost:8000` in your web browser - you should see the familiar homepage! 

You can log in to xbrowse with username `admin` and password `admin`. 

### Loading a Project

However, this homepage won't have any data. 
Now we'll go through the process of actually adding a project that you can use for testing. 

First, log in to the "server", which is actually just the virutal machine on your laptop: 

	vagrant ssh

Pretty cool, eh! before you do anything, run the following: 

	source ~/xbrowse.sh

That just moves you to the right directory, and activates the appropriate python virtual environment. 

Now you can run command line utilities that manage an xbrowse instance. 
We'll first create a project using the `add_project` command. We'll call the project `1kg`: 

	./manage.py add_project 1kg

Now step back out to your *host machine's browser* and visit localhost:8000 again. See the project there? 
Of course there is no data, though. 

To add data to the project, run the following: 

	./manage.py add_individuals_to_project 1kg --fam-file /home/vagrant/1kg.ped
	./manage.py set_vcf 1kg /home/vagrant/1kg.vcf 

That adds these pedigrees to the project and assigns "sets" a VCF file to them. 
Just one more command - we have to load the VCF file into a database that allows fast access. 
Alas, this is the time intensive step, and can take a couple hours: 

	./manage.py reload 1kg 

## Development

See *code organization* above - the application code is located in two directories, `code/xbrowse` and `code/xbrowse-web`. 
Note that these are not git submodules - they are included in .gitignore and are totally separate repositories. 

## Troubleshooting

- Note that the provsioning process is unfortunatley not idempotent. (Does idempotent have an antonym?)
If the provisioning process breaks, it's  best to destroy and rebuild the virutal machine. (`vagrant destroy` then `vagrant up` again) 
Of course, if the error recurs, open an issue. 

- The most common error after provisioning occurs (nondeterministically) when you lose an internet connection - sometimes the guest machine will lose a network connection too that can't be repaired. If this happens, run `vagrant reload` - this restarts the VM. 

- This development version deos need an internet connection (though this is an open issue)
