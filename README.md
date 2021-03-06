[![Coverage Status](https://coveralls.io/repos/github/QualiSystems/Ansible-Shell/badge.svg?branch=develop)](https://coveralls.io/github/QualiSystems/Ansible-Shell?branch=develop)
[![Code Climate](https://codeclimate.com/github/QualiSystems/Ansible-Shell/badges/gpa.svg)](https://codeclimate.com/github/QualiSystems/Ansible-Shell)
[![Dependency Status](https://dependencyci.com/github/QualiSystems/Ansible-Shell/badge)](https://dependencyci.com/github/QualiSystems/Ansible-Shell)

# Ansible-Shell-Extended
This repo is an extension of the official cloudshell configuration management package.  
The base python cloudshell package has been extended for app configuration management to support gitlab private repos. 
A 2G service leveraging the same base package is also included for use with physical resources. 

See our [dev guide](https://devguide.quali.com/configmanagement/2020.1.0/cf-ansible.html) for further info on Ansible Configuration Management development.

## Gitlab Private Repo Support
- Gitlab links are supported, but for Private Repos require the URL to be in format of their REST api
  - `http://<SERVER_IP>/api/<API_VERSION>/projects/<PROJECT_ID>/repository/files/<PROJECT_PATH>/raw?ref=<GIT_BRANCH>`
  - example - `http://10.160.7.7/api/v4/projects/4/repository/files/hello_world.yml/raw?ref=master`
- The password field needs to be populated with gitlab access token, which will be sent along with request as header
- Access Token only needed for private repos, password field can be left blank for public repos
- The "User" field can be left blank for gitlab auth. Only access token needed.
- Public Gitlab Repos work with both "raw" url link AND api-formatted URL with no token passed
- [Gitlab docs](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html)

## To Install Package
- Download python package from releases and place in local pypi server on Quali Server
    - Path: `C:\Program Files (x86)\QualiSystems\CloudShell\Server\Config\Pypi Server Repository`
- Delete venv (if it exists) to force creation of new venv with updated package
    - Path: `C:\ProgramData\QualiSystems\venv\Ansible_Driver_<DRIVER_UID>`

# Ansible 2G Service For Physical Resources
This is a 2G wrapper around the cloudshell ansible package. 
It allows to run ansible playbooks against physical resources as well as deployed app resources.
This service shell uses the same python package as the 1G shell.  

## How to use 2G Shell
- Upload 2G shell package to cloudshell in Manage > Shells > Import section
- Add service to your sandbox and populate required attributes (see attributes below for details)
- Connect to host resources (connect to 'root' of host resource if ports are present)
- Run Execute Playbook Command (details below about options to pass playbook path)

## 2G Service Attributes
|Attribute Name|Data Type|Description|
|:---|:---|:---|
|Playbook URL Full|String|Full path URL of script. For Github can be "raw" url. For gitlab, pass Rest API formatted url. Populate either this or base path + script path|
|Playbook Base Path|String|Base URL to script. This path will join with script path passed to execute playbook command.|
|Playbook Script Path|String|Path to script from root of repo. This will join with base path to create full URL.|
|Connection Method|String|Lookup values \[ssh, winrm, network_cli\] - Type of ansible connection used|
|Address|String|**(Optional)** Address of Script Repo Server. Can be useful to see this on component or generate web link.|
|Repo User|String|**(Optional)** Source Control user for private repo authentication. Required for Github Private Repo. For Gitlab user not required, only access token in password field.|
|Repo Password|Password|**(Optional)** Source Control password for private repo authentication. For GitLab, add private access token here.|
|Script Parameters|String|**(Optional)** Variables accessible to playbook. These are populated in ansible "VARS" file. Pass in following format - key1,val1;key2,val2.|
|Inventory Groups|String|**(Optional)** Designating groups in playbook to be executed. Pass as comma separated string (group1, group2, group3). See Dev guide for more info.|
|Ansible CMD Args|String|**(Optional)** Additional arguments appended to ansible-playbook command line execution. Pass full string(ex. `ansible-playbook -i hosts.ini <ANSIBLE CMD ARGS>`|
|Timeout Minutes|Integer|**(Optional)** Minutes to wait while polling target hosts. Default - 10|
|Gitlab Branch|String|**(Optional)** Defaults to master branch. This attribute relevant for downloading from non-master branches in Gitlab repos.|
|Ansible Config Selector|String|**(Optional)** An alternative to connectors. Create and match this attribute value on target resources. Both matching selector and connected resources will run together. |

## Commands
|Command|Description|
|:-----|:-----|
|Execute Playbook|Run playbook against connected resources.<br>**Playbook Path** (String): path to the playbook in script repo. Options for passing playbook path in next section<br>**Script Params** (String): This will over-ride the service config attribute when passed here. See attribute for more info.|
|Execute Infrastructure Playbook <br>**Hidden Command**| Run playbook against ANY cloudshell resources by passing resource names. This include those not in reservation.<br>**Infrastructure Resources** (String): Pass a comma separated list of Resource Names (Resource1, Resource2, Resource3)<br>**Playbook Path** (String): Same as default command<br>**Script Params** (String): Same as default command|


## Passing Playbook Path Argument
There are a few ways to pass the playbook path to the command.
1. Pass the full URL to command input. This takes precedence over service attributes.
2. Pass playbook path (relative to root of repo) to command. This will join together with base path attribute on service.
3. Pass no command input, will fall back to Repo Full URL if populated, if not populated will fall back to base repo + script path attributes on service.

Note: - `/raw?ref=<GIT_BRANCH>` can be left off url path for Gitlab URL on 2G shell, the shell will add this

## Over-riding Service with Resource Attributes
The service by default will "broadcast it's attributes to all connected resources. 
If select attributes are present AND populated on resource it will override the service level attribute. 
These attributes need to be added to system as global attribute and attached to desired resource models.

The following attributes are supported for over-ride:
- `Connection Method` - Lookup - Create a lookup variable with values \[SSH, WinRM\]
- `Script Parameters` - String - to pass different params to different hosts
- `Inventory Groups` - String - target different inventory group logic for different hosts

## Optional Implementations
- Add "Supports Ansible" Execution Server Selector. This is the same selector that 1G service uses to define your pools of servers that will run script.
  - can be combinded with standard selector to further define your selectors per service
- Create web link to script server by adding the following to UniversalSettings.xml on Quali Server and populating `Address` attribute on service:
  - `<key name="Web Link" pattern="http://{Address}" icon-key="Web"/>`


## Changelog
- 25/12/2020 - Added Gitlab Support & Parameter Over-rides
- 07/01/2021 - Added 2G Service package for physical resources & deployed app resources
- 17/01/2021 - Added support for Ansible List and Hash Variables (by passing JSON)
