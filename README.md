# llmine_core

LLMine is an Open Source tool that helps you mine insights from unstructured text content using configured LLM prompts without writing code. This project contains the source code for LLMine's core service written in Django.

## Who is it for and what can I do with it?

LLMine is intented for use by

1. Software Developers building LLM based workflows to build AI powered apps on top of it.
2. Semi-technical users familiar with LLM prompting techniques to setup quick LLM based workflows for mining unstructured text data without any coding.

Here's some of the things you can build with LLMine

1. **Customer Review Analysis** - You can configure LLMIne prompt chains to find customer sentiments, pain points, severity and topic modelling whenever a customer writes a review somewhere. The results from running the prompts are stored in our database, tagged with the reviews, viewable in our dashboard and available via APIs. You could then make custom applications like BI dashboards, alerting or raising tickets based on these insights mined using the LLMine chains.
2. **Resume Parsing Chains** - You can easily setup an LLMine prompt chains to run whenever a Job Applicant submits a resume. You can find and annotate if the candidate passes some criteria, generate a write-up / summary about the Candidate's fit with the role and so on, without any coding required. Please note, uses of some LLMs in employment related use-cases are not permitted. Please refer to Usage Policies of the underlying LLM you are using. It is upto you to make sure that you comply with all regulatory requirements for your use-case.

And many more...We would love to see the community come up use-cases beyond our original imagination.

## Supported Large Language Models

Our application is best suited to run with Instruction-Tuned LLMs like GPT-3.5 or GPT-4, LLAMA 2 Chat models and so on. As of now we only support OpenAI models, but we are committed to bring support for Open Source LLMs. We believe, the industry is going to use custom fine tuned Llama2 type models for many use cases and we are working to make room for LLMine to utilize them.

* [X] OpenAI GPT-3.5 and GPT-4 all models out of the box
* [ ] LLama2 7B-chat, 13B-chat, 70B-chat
* [ ] Users can add custom models without adding anything in code

## How does it work?

1. **Create a Content Pool** - First step is to define a Content Pool. Let's say we create one called *Amazon Reviews*
2. **Setup Extracter Chains for a Content Pool** - Now we can define one or more extracter chains for our content pool. We can define what underlying LLM we want to use for a particular chain. Let's say we define a chain called *Issue Extracter* for our *Amazon Reviews* pool.
3. **Create Extracter Prompts under the chains** - Now that you have defined a chain, you can actually create prompts that define the tasks to perform on the Ingested Text Content you receive in the Content Pool. For example, we create three prompts like follows
   * issue_type -> "Is this review a complaint, compliment or a suggestion?", Responds as ["Complaint, "Compliment", "Suggestion", "Other"]
   * issue_severity -> "How severe does this complaint look like?", Responds as ["Critical", "High", "Medium", "Low"], run if (issue_type == "Complaint")
   * product_tag -> "What product does the customer talk about?", Responds as ["Product 1", "Product 2"]
   * summary -> "Summarize the review in bullet points", Responds with JSON with a given schema
4. **Set up webhooks to ingest the content and see the magic** - You can push your reviews to the content pool using a webhook. The extracter chains will run on your content after you push your text content to the pool. These data will be stored in our database and will be available for further use.
5. **Use the mined insights** - Now that our chains have mined all the required details from the text, you can analyze them on a dashboard, export them or consume via our REST APIs in downstream applications.

## Product Roadmap

* [X] Basic Functionality usable via Django Admin Panel
* [X] Out-of-the-box support for OpenAI models
* [X] Choices Return, JSON Return and Text Return types configurable
* [X] Conditionally run prompts based on the output of previous prompts in a chain
* [ ] Webhooks and REST API Layer
* [ ] User-Friendly UI to configure workflows
* [ ] Basic Dashboard to view and export extracted insights
* [ ] LLama2 Support
* [ ] Text Clustering and Theme Modelling Support on Content Pool level

Code contributions or help with testing and documentation from the community are welcome. Your feedback on how you plan to use LLMine will help us refine and prioritize our roadmap better.

## Usage Documentation

Work in Progress, Coming Soon!

## How to run in local for development?

First you need to clone the project and setup the Python/Django Environment. You will also need a PostgreSQL database, OpenAI API key and a Redis server to run this project in dev.

```
$ git clone git@github.com:LLMine/llmine_core.git
$ cd llmine_core
$ python3.10 -m venv env
$ source env/bin/activate
(env)$ pip install -r requirements.txt
```

Now create a .env file in the repository containing the following env vars.

```
DB_HOST=<YOUR DB HOSR>
DB_USER=<YOUR DB USER>
DB_PASSWORD=<YOUR DB PASSWORD>
DB_PORT=<YOUR DB PORT>
DB_NAME=<YOUR DB NAME>
SECRET_KEY=<DJANGO SECRET KEY, PLEASE GENERATE YOUR OWN>
DEBUG=True
OPENAI_API_KEY=<OPEN AI KEY>
REDIS_URL=<YOUR REDIS URL>
```

Now you need to export these vars on your command line, run migrations, create a superuser and login via admin panel.

```
(env)$ source export_env_vars.sh
(env)$ python manage.py migrate
(env)$ python manage.py createsuperuser
(env)$ python manage.py runserver
```

You will need to run the celery too in a different terminal to actually run the extracter chain processing tasks.

```
(env)$ source export_env_vars.sh
(env)$ celery -A llmine_core worker -l info --concurrency=2
```

## Contribution Guide

Work in Progress

## Special Thanks

Speical thanks to Vulmiqi (vulmiqi.com) for sharing cloud resources and OpenAI credits with the authors of this project, for testing and debugging purposes.

![Vulmiqi Logo](https://vulmiqi.com/img/logo1.png)
