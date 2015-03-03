"""
This is a script to parse a text file that contains a commit log in pretty-format.
"""

from sys import argv
import re
import json

''' Creates a dictionary named commits_dict made up of dictionaries. 

The outer dictionary key is a sequential commit number (0, n). 
The outer dictionary's value is one commit.

Each inner dictionary is one commit whose keys are 'A', 'M', or 'D'.
Each inner dictionary's values are a list of the files that were Added, Modified, or deleted.
'''
def parse_log_to_dict(filename):
    i = 0
    commits_dict = {}
    pattern = re.compile('[A|D|M]\t')


    with open(filename, 'r') as f:
      for line in f:
        match = pattern.match(line)

        if line.startswith('commit '):
          single_commit = {}
          commits_dict[i] = single_commit
          i = i+1

        if match is not None:
          print '         FOUND'
          commit_process_key, commit_file_affected = line.split('\t', 1)

          if commit_process_key in single_commit:
            single_commit[commit_process_key].append(commit_file_affected.rstrip())
          else:
            single_commit[commit_process_key.strip()] = [commit_file_affected.rstrip()]


    f.close()

    # reverse keys so commit 0 is the first commit
    ordered_commits_dict = {}
    j = len(commits_dict)-1 
    for key in commits_dict:
      ordered_commits_dict[j] = commits_dict[key]
      j = j-1

    del commits_dict
    return ordered_commits_dict
    
    

def main():
    filename = '/Users/rxdt/log.txt'

    commits_dict = parse_log_to_dict(filename)
    print commits_dict

    with open('commits_json.txt', 'w') as outfile:
      outfile.write(unicode(json.dumps(commits_dict, sort_keys=True, indent=2)))



if __name__ == "__main__":
    main()

