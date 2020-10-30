from prompt_toolkit.shortcuts import radiolist_dialog

import click


@click.command()
@click.argument('path')
def remove(path):
    try:


        repo = Repo(path)

        subs = repo.submodules

        missing = []

        found = []

        dlist = []

        for sub in subs:
            if sub.module_exists():
                found.append(sub)
            else:
                missing.append(sub)
            dlist.append((sub, sub.path))

        if len(dlist) > 0:
            result = radiolist_dialog(
                title=path,
                text="Which submodule would you like to remove",
                values=dlist).run()

            if result is not None:
                path = result.path
                sub = result.remove(force=True)
                print(f"Removed submodule: {path}")
            else:
                print("aborting...")
        else:
            print("No submodules in project")
    except InvalidGitRepositoryError:
        print("not a valid repository")


if __name__ == '__main__':
    remove()
