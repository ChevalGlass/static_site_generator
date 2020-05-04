# Static Site Generator
Generate a static web site from template files and content written in markdown.

This is my generic static site generator.

This uses python and the markdown module to convert pages written in markdown into html pages.
Each page of the site should have a main .md file with a .json meta data file of the same name.

The meta data includes:
- Page title.
- List of additional css files.
- Lis tof additional js files.


Running the script with the -h flag will show the help and list all the options.

The current features are:
- Specify a template file. (Default: master_template.html)
- Specify the directory the site is in. (Default: current directory)
- Specify the name of the folder in the site where the .md files are. (Default: docs_md)
- Specify the site suffix for the title of each page. (Will show up after the title specified in the meta data file.)

Planned features:
- Specify the site prefix for the title of each page. (Will show up before the title specified in the meta data file.)
- A site navigation cache to allow updating a single page instead of the whole site.

## Example site structure.
.
├── docs
│   ├── index.html
│   └── pages
│       └── example_page.html
├── docs_md
│   ├── index.json
│   ├── index.md
│   └── pages
│       ├── example_page.json
│       └── example_page.md
├── master_template.html
└── styles
