# How to generate post

Select which posts you want to generate. For example, to generate the the state of the union post, you would run the script from this directory and pass the post name as an argument:

```shell
$ bash run.sh state_of_union
```

The bash script will:

1. Build docker image and tagging it
2. Run the docker image, taking the RMarkdown file and rendering it into html and md
3. Copy the output md to readme.md file so that it appears in github at the project directory level