# The Jor1k Filesystem

The `sysroot` directory contains the filesystem loaded at runtime by
the Jor1k virtual machine used in
[sysbuild](https://github.com/cs-education/sysbuild).

The `sysroot` directory actually contains the
[s-macke/jor1k-sysroot](https://github.com/s-macke/jor1k-sysroot/) Git
repository within this repository, managed using
[Git subtree merges](https://help.github.com/articles/about-git-subtree-merges/).
This allows full control and editing of the filesystem, while also
helping to keep in sync with updates and changes to the upstream
repository.

To work with this setup, you need to add a new Git remote:
```sh
$ git remote add -f s-macke-jor1k-sysroot https://github.com/s-macke/jor1k-sysroot.git
```

Then use specific commands to fetch and merge updates:

* To compare what is in your `jor1kfs/sysroot` subdirectory with what
  the master branch on the upstream was the last time you fetched, you
  can run:
    ```sh
    $ git diff-tree -p s-macke-jor1k-sysroot/master
    ```

* To update the subproject with the upstream changes:
    ```sh
    $ git pull -s subtree --squash --no-commit s-macke-jor1k-sysroot master
    ```
    Note: You need to perform a commit manually after the merge.
