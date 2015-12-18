from bitbucket.bitbucket import Bitbucket
from github import Github
from config import github_user, github_pass, bit_user, bit_pass
import os

g = Github(github_user, github_pass)
bb = Bitbucket(bit_user, bit_pass)


def clean_bit():
    _, repos = bb.repository.all()
    for repo in repos:
        _, repo = bb.repository.delete(repo['name'])


def list_repo(org):
    for repo in g.get_organization(org).get_repos():
        print repo.name
        yield repo.name


def clone_repo(org):
    for name in list_repo():
        bb.repository.create(name)
        os.system('git clone --mirror https://%s:%s@github.com/%s/%s.git' % (
            github_user, github_pass, org, name))
        os.chdir('%s.git' % name)
        os.system('git remote set-url --push origin https://%s:%s@bitbucket.org/%s/%s.git' % (
            bit_user, bit_pass, bit_user, name
        ))
        os.system("git push --mirror")

if __name__ == "__main__":
    import clime.now
