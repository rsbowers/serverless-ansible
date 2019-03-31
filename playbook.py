#!/usr/bin/python

import json
from collections import namedtuple

from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from ansible.executor.playbook_executor import PlaybookExecutor

def playbook(**kwargs):

  loader = DataLoader()
  inventory = InventoryManager(loader=loader, sources='localhost,')
  variable_manager = VariableManager(loader=loader, inventory=inventory)
  playbook_path = 'playbook.yml'

  Options = namedtuple(
    'Options',
    [
      'connection',
      'remote_user',
      'ask_sudo_pass',
      'verbosity',
      'ack_pass', 
      'module_path', 
      'forks', 
      'become', 
      'become_method', 
      'become_user', 
      'check',
      'listhosts', 
      'listtasks', 
      'listtags',
      'syntax',
      'sudo_user',
      'sudo',
      'diff'
    ]
  )
  
  options = Options(
    connection='smart', 
    remote_user=None,
    ack_pass=None,
    sudo_user=None,
    forks=5,
    sudo=None,
    ask_sudo_pass=False,
    verbosity=5,
    module_path=None,  
    become=None, 
    become_method=None, 
    become_user=None, 
    check=False,
    diff=False,
    listhosts=None,
    listtasks=None, 
    listtags=None, 
    syntax=None
  )

  passwords = {}

  pbook = PlaybookExecutor(
    playbooks=[playbook_path],
    inventory=inventory,
    loader=loader,
    options=options,
    variable_manager=variable_manager,
    passwords=passwords
  )

  out = pbook.run()

  return out


def handler(event, context):

  playbook_output = playbook()

  body = {
      "message": "Ansible runner successful",
      "output": playbook_output
  }

  response = {
      "statusCode": 200,
      "body": json.dumps(body)
  }

  return response
