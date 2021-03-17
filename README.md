# *datagen*
#### This project contains a number of Python files that do a variety of different tasks. These tasks are to first extract wiki-dump files into small, stripped-down html files free from links, pictures, and special characters. Then local web links are generated and appended to the html files in a hierarchal manner, several levels deep. Continuing on to the next task, the html files are sorted into a large hierarchal tree of directories with the same associated, generated links like in the first task, except with the appropriate directory path.

#### The smaller tasks include generating XML files with generated links in the first task, then a task generating a random query list of words from all the html files created in the first task, and finally a task that generates JSON files containing information and specified facets for each of the html files as generated in the first task.

#### While some of these tasks were tailored for performance testing and website crawling using an EC2 server on AWS with an S3 bucket to store and host the html files, this project is for anyone to use as they wish. Feel free to use and manipulate the code as desired.

*Caution: Links generated and appended to the html files will not work on a local disk unless the code is manipulated to do so. As described above, these html files were tested with an AWS EC2 server containing an S3 bucket in which case the links worked as intended.*

### Argument Key

`-if` or `--inputfile`

`-of` or `--outputfile`

`-id` or `--inputdir`

`-od` or `--outputdir`

*Note: If help is needed to understand what to type in a command, begin typing `python3` followed by whatever file being worked on ex. `cleanup.py` with an `-h` after it.*

*Example:*
```
python3 htmlclean.py -h
```

*Note: The instructions in this README file is more of a follow-along, feel free to copy and paste the `highlighted` examples to see what each step does. Otherwise, feel free to tweak it if necessary.*

#
#
# *Best results happen when steps are followed in order -- #1 is required, the rest are optional*
#

# **#1**
### **Downloading, cleaning, and generating static links with  archived wikipedia files**
#

### **Step 1:**
**--> Downloading archived wikipedia files <--**

*Website link to archived wikipedia files (reference, not used for examples):*
```
ftp://ftpmirror.your.org/pub/wikimedia/dumps/enwiki/
```

Please use examples throughout the instruction set for a better understanding of what is happening. For step 1, `Example1` links will be used and will contain two small 11-30ish MB `.bz2` files. If there's a desire to download all the files, use the `Example2` link.

**Highlight, copy, and paste examples below into a Terminal-based application**

*Example1 (2 links that download 2 small sample files):*
```
wget -P wiki_dumps ftp://ftpmirror.your.org/pub/wikimedia/dumps/enwiki/latest/enwiki-latest-pages-articles14.xml-p7697599p7744799.bz2
```
```
wget -P wiki_dumps ftp://ftpmirror.your.org/pub/wikimedia/dumps/enwiki/latest/enwiki-latest-pages-articles26.xml-p42567204p42663461.bz2
```

*Caution: `Example2` will take up several gigabytes of disk space*

*Example2 (optional, link to download all files):*
```
wget -P wiki_dumps ftp://ftpmirror.your.org/pub/wikimedia/dumps/enwiki/latest/enwiki-latest-pages-articles[0-9].xml-p*.bz2
```


### **Step 2:**
**--> Extracting raw html files into stripped and cleaned html files <--**

#### First
Make sure the directory containing the `bz2` files are in the directory with all the datagen python files being used.

#### Second
Next, generate the raw (untouched) `html` files from the directory containing the `bz2` files using a slightly modified script of extraction code created by **Giuseppe Attardi** and his fellow contributors.

#### Arguments
+ First, `for file in wiki_dumps/*.bz2;` and `n=$((n+1))` mean that however many `bz2` files in the desired directory containing them, it will make sure to use all of them and organize each `bz2` file as part of a list of incrementing folders.
+ Second, `python3 htmlextract.py` means that python (specifically python 3) will run the python script `htmlextractor.py`.
+ Third, `-o ds1rawhtml/$n --html -b 25K $file` means that the output will be directed to the directory created in html format with a size of 25 KB per file.

*Example:*
```
for file in wiki_dumps/*.bz2;
do
    n=$((n+1))
    python3 htmlextract.py -o ds1rawhtml/$n --html -b 25K $file &
done
```

*Note: If running this command more than once for other purposes in the same terminal window, it will save the `n` variable and therefore will continue to increment the directory names upon the last time the command was used.*

#### Third
This will generate clean html files that will clean up unnecessary text, symbols, and links.

#### Arguments
+ First, use the directory `ds1rawhtml` containing the raw html files.
+ Second, use the directory `ds1` to put all the cleaned html files in.

*Example:*
```
python3 htmlclean.py -id ds1rawhtml -od ds1
```

*Note: This process could take quite some time depending on how many and how big the `bz2` files are.*

### **Step 3:**
**--> Creating a file containing a list of file paths <--**

#### Arguments
+ First, use the directory `ds1` containing the cleaned html files.
+ Second, create a new name for the text file ex. `ds1filepathlist.txt` that will contain all the file paths.

*Example:*
```
python3 htmlpathlist.py -id ds1 -of ds1filepathlist.txt
```

### **Step 4:**
**--> Creating a file containing a list of links with file paths <--**

#### Arguments
+ First, use the directory `ds1` containing the cleaned html files.
+ Second, create a new name for the text file ex. `ds1filelinklist.txt` that will contain all the URL links in relation to their file paths.

*Example:*
```
python3 htmllinklist.py -id ds1 -of ds1filelinklist.txt
```

### **Step 5:**
**--> Appending a hierarchy of static links onto multiple html files <--**

*Note: This will make changes to the directory containing the cleaned html files. Make a backup original copy from the example below.*

Use the directory `ds1` containing the cleaned html files and then the new name of the original copy ex. `ds1_original`

*Example:*
```
cp -r ds1 ds1_original
```

*Note: This script will go in a specific order from the `python3` file we are about to run. It will have a `root` file containing `100 links` at the end of the file. Then, the next `10 files` will contain `10 links` each. Then, the next `100 files` will contain `10 links` each. So on an so forth.*

#### Arguments
+ First, use the file `ds1filepathlist.txt` containing the list of file paths.
+ Second, use the file `ds1filelinklist.txt` containing the list of links with their corresponding file paths.

*Example:*
```
python3 htmlappendlink.py -if ds1filepathlist.txt -if1 ds1filelinklist.txt
```

### **Step 6:**
**--> Properly format each html file for future validation testing <--**

#### Arguments
+ First, use the file `ds1filepathlist.txt` containing the list of file paths.

*Example:*
```
python3 htmlformat.py -if ds1filepathlist.txt
```

*Note: This could take a while depending on how big and how many files are being used.*

To see if it worked, click on the first file `00.html` inside the `ds1` directory. Scroll to the bottom and it should show `100 links` added to the file.


# **#2**
### **Restructuring hierarchy with new file paths and links**
#

### **Step 1:**
**--> Move files from one temporary directory to the other <--**

Create a temporary copy `ds1tmp` of the original directory `ds1_original` created earlier.

*Example:*
```
cp -r ds1_original ds1tmp
```

#### First
Make sure all the generated text files and directories are still in the main directory from the process above. They will be needed!

#### Arguments
+ First, use the temporary directory `ds1tmp` just created.
+ Second, move the files into another temporary directory `ds4tmp` that will contain all the cleaned html files without subdirectories.

*Example:*
```
python3 htmlrestructure.py -id ds1tmp -od ds4tmp
```

Then delete the temporary directory `ds1tmp` since it's now empty.

*Example:*
```
rm -r ds1tmp
```

### **Step 2:**
**--> Creating a file containing a list of file paths for temporary directory <--**

#### Arguments
+ First, use the temporary directory `ds4tmp` containing the cleaned html files.
+ Second, create a new name for the temporary text file ex. `ds4tmpfilepathlist.txt` that will contain all the file paths.

*Example:*
```
python3 htmlpathlist.py -id ds4tmp -of ds4tmpfilepathlist.txt
```

### **Step 3:**
**--> Creating a hierarchal directory structure 5-6 levels deep <--**

#### Arguments
+ First, create a new directory ex. `ds4` that will contain all the subdirectories/facets.
+ Second, determine the number of directories ex. `100000`

*Example:*
```
python3 htmlfacetdir.py -iname ds4 -inum 100000
```
### **Step 4:**
**--> Creating a file containing a list of file paths for new directory <--**

#### Arguments
+ First, use the directory `ds4` containing the cleaned html files.
+ Second, determine the number of files ex. `100000`
+ Third, create a new name for the text file ex. `ds4filepathlist.txt` that will contain all the URL links in relation to their file paths.

*Example:*
```
python3 htmlfacetdirpathlist.py -iname ds4 -inum 100000 -of ds4filepathlist.txt
```

### **Step 5:**
**--> Copy files from temporary directory to the new directory <--**

#### Arguments
+ First, we will need the temporary text file `ds4tmpfilepathlist.txt` containing the file paths of the temporary directory `ds4tmp`
+ Second, we will need the new text file `ds4filepathlist.txt` containing the new file paths of the directory `ds4`

*Example:*
```
python3 htmlcopy.py -if ds4tmpfilepathlist.txt -if1 ds4filepathlist.txt
```

### **Step 6:**
**--> Creating a file containing a list of links with file paths of new directory <--**

#### Arguments
+ First, use the directory `ds4` containing the cleaned html files.
+ Second, determine the number of files ex. `100000`
+ Third, create a new name for the text file ex. `ds4filelinklist.txt` that will contain all the URL links in relation to their file paths.

*Example:*
```
python3 htmlfacetdirlinklist.py -iname ds4 -inum 100000 -of ds4filelinklist.txt
```

### **Step 7:**
**--> Appending a hierarchy of static links onto multiple html files <--**

*Note: This will make changes to the directory containing the cleaned html files. Make a backup original copy from the example below.*

Use the directory `ds4` containing the cleaned html files and then the new name of the original copy ex. `ds4_original`

*Example:*
```
cp -r ds4 ds4_original
```

*Note: This script will go in a specific order from the `python3` file we are about to run. It will have a `root` file containing `100 links` at the end of the file. Then, the next `10 files` will contain `10 links` each. Then, the next `100 files` will contain `10 links` each. So on an so forth.*

#### Arguments
+ First, use the file `ds4filepathlist.txt` containing the list of file paths.
+ Second, use the file `ds4filelinklist.txt` containing the list of links with their corresponding file paths.

*Example:*
```
python3 htmlappendlink.py -if ds4filepathlist.txt -if1 ds4filelinklist.txt
```

### **Step 8:**
**--> Properly format each html file for future validation testing <--**

#### Arguments
+ First, use the file `ds4filepathlist.txt` containing the list of file paths.
+ Second, there's a way to format the html documents **without** the metadata as facets, that is, use the first example.

*Note: The first example will NOT use the following text files `type.txt`, `file_extension.txt`, `company.txt`, `name.txt`, and `filename.txt`. These files are specifically for the second example.*

*Note: Depending on what is desired, it's best to **chose one or the other to execute**. Look at examples below to see what the results look like.*

**IMPORTANT: This first example will add the following information at the beginning and ending of each file in `ds4`.**

*Note: the `<title>...</title>` tag information will be different per file.*

**Beginning:**
```
<!DOCTYPE html>
<html>

<head>
<meta charset="UTF-8">
<title>ds4/1/1/1/1/1/1.html</title>
</head>

<body>

...(CONTENT OF FILE)...
```

**Ending:**
```
...(CONTENT OF FILE)...
</body>
</html>
```

*Example1:*
```
python3 htmlformat.py -if ds4filepathlist.txt
```

### **OR**

**IMPORTANT: This second example will add the following information at the beginning and ending of each `html` file in `ds4`.**

*Note: the `<meta>` and `<title>...</title>` information will be different per file.*

**Beginning:**
```
<!DOCTYPE html>
<html>

<head>
<meta charset="UTF-8">
<meta name=type content="window"/>
<meta name=file_extension content=".class"/>
<meta name=company_name content="Pilgrim's Pride"/>
<meta name=created_by_name content="Yvonne Rutherford"/>
<meta name=file_name content="the_yet"/>
<title>ds4/1/1/1/1/1/1.html</title>
</head>

<body>

...(CONTENT OF FILE)...
```

**Ending:**
```
...(CONTENT OF FILE)...
</body>
</html>
```

*Example2:*
```
python3 htmlformat2.py -if ds4filepathlist.txt
```

*Note: This could take a while depending on how big and how many files are being used.*

To see if it worked, click on the first file `1.html` inside the `ds4` directory. Scroll to the bottom and it should show `100 links` added to the file.


# **#3**
### **Generating dynamic links with html files containing javascript code**
#

### **Step 1:**
**--> Move files from one temporary directory to the other <--**

Create a temporary copy `ds1jstmp` of the original directory `ds1_original` created earlier.

*Example:*
```
cp -r ds1_original ds1jstmp
```

#### First
Make sure all the generated text files and directories are still in the main directory from the process above. They will be needed!

#### Arguments
+ First, use the temporary directory `ds1jstmp` just created.
+ Second, move the files into another temporary directory `ds4jstmp` that will contain all the cleaned html files without subdirectories.

*Example:*
```
python3 htmlrestructure.py -id ds1jstmp -od ds4jstmp
```

Then delete the temporary directory `ds1jstmp` since it's now empty.

*Example:*
```
rm -r ds1jstmp
```

### **Step 2:**
**--> Creating a file containing a list of file paths for temporary directory <--**

#### Arguments
+ First, use the temporary directory `ds4jstmp` containing the cleaned html files.
+ Second, create a new name for the temporary text file ex. `ds4jstmpfilepathlist.txt` that will contain all the file paths.

*Example:*
```
python3 htmlpathlist.py -id ds4jstmp -of ds4jstmpfilepathlist.txt
```

### **Step 3:**
**--> Creating a hierarchal directory structure 5-6 levels deep <--**

#### Arguments
+ First, create a new directory ex. `ds4js` that will contain all the subdirectories/facets.
+ Second, determine the number of directories ex. `100000`

*Example:*
```
python3 htmlfacetdir.py -iname ds4js -inum 100000
```
### **Step 4:**
**--> Creating a file containing a list of file paths for new directory <--**

#### Arguments
+ First, use the directory `ds4js` containing the cleaned html files.
+ Second, determine the number of files ex. `100000`
+ Third, create a new name for the text file ex. `ds4jsfilepathlist.txt` that will contain all the URL links in relation to their file paths.

*Example:*
```
python3 htmlfacetdirpathlist.py -iname ds4js -inum 100000 -of ds4jsfilepathlist.txt
```

### **Step 5:**
**--> Copy files from temporary directory to the new directory <--**

#### Arguments
+ First, we will need the temporary text file `ds4jstmpfilepathlist.txt` containing the file paths of the temporary directory `ds4jstmp`
+ Second, we will need the new text file `ds4jsfilepathlist.txt` containing the new file paths of the directory `ds4js`

*Example:*
```
python3 htmlcopy.py -if ds4jstmpfilepathlist.txt -if1 ds4jsfilepathlist.txt
```

### **Step 6:**
**--> Creating a file containing a list of links with file paths of new directory <--**

#### Arguments
+ First, use the directory `ds4js` containing the cleaned html files.
+ Second, determine the number of files ex. `100000`
+ Third, create a new name for the text file ex. `ds4jsfilelinklist.txt` that will contain all the URL links in relation to their file paths.

*Example:*
```
python3 htmlfacetdirlinklistjs.py -iname ds4js -inum 100000 -of ds4jsfilelinklist.txt
```

### **Step 7:**
**--> Appending a hierarchy of static links onto multiple html files <--**

*Note: This will make changes to the directory containing the cleaned html files. Make a backup original copy from the example below.*

Use the directory `ds4js` containing the cleaned html files and then the new name of the original copy ex. `ds4js_original`

*Example:*
```
cp -r ds4js ds4js_original
```

*Note: This script will go in a specific order from the `python3` file we are about to run. It will have a `root` file containing `100 links` at the end of the file. Then, the next `10 files` will contain `10 links` each. Then, the next `100 files` will contain `10 links` each. So on an so forth.*

#### Arguments
+ First, use the file `ds4jsfilepathlist.txt` containing the list of file paths.
+ Second, use the file `ds4jsfilelinklist.txt` containing the list of links with their corresponding file paths.

*Example:*
```
python3 htmlappendlinkjs.py -if ds4jsfilepathlist.txt -if1 ds4jsfilelinklist.txt
```

### **Step 8:**
**--> Properly format each html file for future validation testing <--**

#### Arguments
+ First, use the file `ds4jsfilepathlist.txt` containing the list of file paths.
+ Second, there's a way to format the html documents **without** the metadata as facets, that is, use the first example.

*Note: the `<title>...</title>` tag information will be different per file.*

**Beginning:**
```
<!DOCTYPE html>
<html>

<head>
<meta charset="UTF-8">
<title>ds4/1/1/1/1/1/1.html</title>
</head>

<body onload="linklist();">

...(CONTENT OF FILE)...
```

**Ending:**
```
...(CONTENT OF FILE)...
</body>
</html>
```

*Example:*
```
python3 htmlformatjs.py -if ds4jsfilepathlist.txt
```

*Note: This could take a while depending on how big and how many files are being used.*

To see if it worked, click on the first file `1.html` inside the `ds4` directory. Scroll to the bottom and it should show `100 links` added to the file.


# **#4**
### **Creating xml formatted sitemap files**
#

### **Step 1:**
**--> Generate sitemap files with proper xml formatting <--**

#### First
Make sure all the generated text files and directories are still in the main directory from the above processes. They will be needed!

#### Arguments
+ First, use the directory `ds1` containing the cleaned html files.
+ Second, create a new name for the `xml` file ex. `ds1sitemap.xml` that will contain all the URL links in relation to their file paths.
+ Finally, use the URL link to add to the file paths. As an example, an AWS server containing a bucket is used ex. `https://s3-us-west-2.amazonaws.com/test.bucket/`

*Note: Emphasis on the `https://` before the actual URL link!*

*Example:*
```
python3 sitemaplinklist.py -id ds1 -of ds1sitemap.xml -u https://s3-us-west-2.amazonaws.com/test.bucket/
```

### **Step 2:**
**--> Divide up and sort urls across multiple sitemap files <--**

#### Arguments
+ First, create a new directory ex. `ds1sitemap` for our `xml` files to go into.
+ Second, use the `xml` file `ds1sitemap.xml` containing all the URLs.

*Example:*
```
mkdir ds1sitemap
```
```
python3 sitemapfilesplit.py -if ds1sitemap.xml
```

*Caution: There will be multiple `xml` files littered in the directory. Once the process is finished, move them into the recently created directory `ds1sitemap` created for the `xml` files.*

*Example:*
```
mv sitemap*.xml ds1sitemap
```

Now there should be properly formatted `xml` files that contain URL links with their respective html file paths from the directory containing html files.


# **#5**
### **Creating a file containing a randomly generated query list**
#

### **Step 1:**
**--> Generate a query list file containing random and duplicated 1, 2, 3, and 4 token words <--**

#### First
Make sure all the generated text files and directories are still in the main directory from the above processes. They will be needed!

#### Arguments
+ First, use the text file `ds1filepathlist.txt` containing the list of file paths created earlier.
+ Second, create a new file ex. `ds1querylist.txt` for the query list.

*Example:*
```
python3 queryrandomlist.py -if ds1filepathlist.txt -of ds1querylist.txt
```

Now there should be a generated, randomized, and duplicated query list of 1-4 token words.


# **#6**
### **Creating json files containing facet data**
#

### **Step 1:**
**--> Creating json files from a file containing a list of json file paths <--**

#### First
Make sure all the generated text files and directories are still in the main directory from the above processes. They will be needed!

#### Second
This will generate all the text into a single text file with proper `json` formatting.

#### Arguments
+ First, create a new directory for the `json` files to go into. One for facets as file paths ex. `ds1jsonfacetpath` and/or one for facets as data ex. `ds1jsonfacetdata` that's been collected via the text files provided.
+ Second, use the file `ds1filepathlist.txt` that contains the file paths of the directory containing all the cleaned html files.
+ Third, create a new file ex. `ds1jsonfacetpath.txt` and/or ex. `ds1jsonfacetdata.txt` as a temporary file containing all the content in `json` format.

*Example1:*
```
mkdir ds1jsonfacetpath
```

```
python3 jsontempfile.py -if ds1filepathlist.txt -of ds1jsonfacetpath.txt
```

### **AND / OR**

*Example2:*
```
mkdir ds1jsonfacetdata
```

```
python3 jsontempfile2.py -if ds1filepathlist.txt -of ds1jsonfacetdata.txt
```

#### Third
This will split the text into multiple files per html file with proper `json` formatting.

#### Arguments
+ First, use the temporary file `ds1jsonfacetpath.txt` and/or `ds1jsonfacetdata.txt` created earlier.

*Caution: There will be a bunch of `json` files littered in the directory. Once the process is finished, move them into the recently created directory created for the `json` files.*

*Caution: Ignore the warnings when running some of the examples below.*

*Example1:*
```
python3 jsonfilesplit.py -if ds1jsonfacetpath.txt
```
```
find . -name "*.json" -maxdepth 1 -exec sh -c 'mv "$@" "$0"' ds1jsonfacetpath {} +
```

### **AND / OR**

*Example2:*
```
python3 jsonfilesplit.py -if ds1jsonfacetdata.txt
```
```
find . -name "*.json" -maxdepth 1 -exec sh -c 'mv "$@" "$0"' ds1jsonfacetdata {} +
```

*Note: This will take awhile depending on how many html files there are.*

#### Fourth
This will generate a list of `json` file paths.

#### Arguments
+ First, use the directory `ds1jsonfacetpath` and/or `ds1jsonfacetdata` containing the json files created earlier.
+ Second, create new file ex. `ds1jsonpathlistfacetpath.txt` and/or ex. `ds1jsonpathlistfacetdata.txt` that will contain all the `json` file paths.

*Example1:*
```
python3 jsonpathlist.py -id ds1jsonfacetpath -of ds1jsonpathlistfacetpath.txt
```

### **AND / OR**

*Example2:*
```
python3 jsonpathlist.py -id ds1jsonfacetdata -of ds1jsonpathlistfacetdata.txt
```

Now there should be a directory containing several `json` files, each containing the correlating html file. Also a text file containing the file paths of all the `json` files that were created in the previous step.
