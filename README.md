
# Table of Contents

1.  [\`path<sub>tree</sub><sub>python</sub>\` Library](#org10d1718)
    1.  [Introduction](#org53879e4)
    2.  [Requirements](#orgbabee4b)
    3.  [Usage](#org9e4ff97)


<a id="org10d1718"></a>

# \`path<sub>tree</sub><sub>python</sub>\` Library


<a id="org53879e4"></a>

## Introduction

path<sub>tree</sub><sub>python</sub> is a python library that resolves filepath and url
into tree struture.


<a id="orgbabee4b"></a>

## Requirements

pathlib, urllib


<a id="org9e4ff97"></a>

## Usage

Examples 

    # Add a node
    from path_tree_python import PTree
    tree = PTree()
    tree.add('http://www.test.org/index.html')
    tree.print()
    
    # ----------------------------
    # 'www.test.org'--'index.html'
    # ----------------------------

     # Add a node & prints
     tree.add('http://www.test.org/test/index.html')
     tree.print()
    
    # ----------------------------
    # 'www.test.org'-----'index.html'
    #                 |__'test'_____'index.html'

    
    # Convert leaf to df sheet
    tree.to_df()
    
    # --------------------------------------------
    # |      root      |   depth 1  |   depth 2  |
    # |----------------|------------|------------|
    # |  wwww.test.org |    test    | index.html |
    # |----------------|------------|------------|
    # |  wwww.test.org | index.html |            |
    # --------------------------------------------

    # Show tree statistics
    tree.stats_df(depth=1, func='count')
    
    # --------------------------------------------
    # |      root      |   depth 1  |   count    |
    # |----------------|------------|------------|
    # |  wwww.test.org |    test    |     1      |
    # |----------------|------------|------------|
    # |  wwww.test.org | index.html |     1      |
    # --------------------------------------------

    # Accept other data types
    tree = PTree(path_attr=lambda x: x['path'])
    tree.add({'path':'www.test.org/hello.html', 'description':'hello page'})
    tree.stats_df(depth=1, func='count')
    
    # --------------------------------------------
    # |      root      |   depth 1  |   count    |
    # |----------------|------------|------------|
    # |  wwww.test.org | hello.html |     1      |
    # --------------------------------------------

    # Accessing the node
    tree = PTree(path_func=lambda x: x['path'])
    tree.add({'path':'www.test.org/hello.html', 'description':'hello page'})
    tree.stats_df(depth=1, func='count')
    
    # --------------------------------------------
    # |      root      |   depth 1  |   count    |
    # |----------------|------------|------------|
    # |  wwww.test.org | hello.html |     1      |
    # --------------------------------------------

