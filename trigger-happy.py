from subprocess import call
import os

#git fsck --cache --unreachable $(git for-each-ref --format="%(objectname)") > derp
output_file = "derp"

with open(output_file) as f:
    content = f.readlines()



filename = "file"
i = 1
for c in content:
    if c.startswith("dangling blob "):

        #generate the file from the git blob
        c = c.replace("dangling blob ", "")
        print "Checking blob %s" % c
        full_file_name = filename + str(i)
        f = open(full_file_name,"wb")
        call("git show %s" % c,stdout=f, shell=True)
        f.close()

        #open the generated file and loop through the file to find out if we should do something with it
        fp = open(full_file_name)
        file_folder = ""
        file_name_to_use = ""
        create_file = False
        app_namespace = False
        test_file = False
        for l, line in enumerate(fp):
            #find the namespace. Generate the folders if it's the App namespace
            if "namespace" in line:
                stripped_namespace = line.replace("namespace", "").replace(";", "").replace("\\", "/").strip()
                if stripped_namespace.startswith("App") or stripped_namespace.startswith("app"):
                    app_namespace = True
                    stripped_namespace_dir = "./%s" % stripped_namespace
                    file_folder = stripped_namespace_dir
                    if not os.path.exists(stripped_namespace_dir):
                        os.makedirs(stripped_namespace_dir)

            #find the file name based off the class name
            if line.startswith("class "):
                splitted = line.split()
                file_name_to_use = splitted[1]
                #additional logic for finding test files
                if "est" in file_name_to_use:
                    test_file = True
                create_file = True

            #abstract classes
            if line.startswith("abstract class "):
                splitted = line.split()
                file_name_to_use = splitted[2]
                create_file = True

            #interfaces
            if line.startswith("interface "):
                splitted = line.split()
                file_name_to_use = splitted[1]
                create_file = True

            #special logic for the routes file
            if line.startswith("| Application Routes"):
                file_name_to_use = "routes"
                stripped_namespace_dir = "./App/Http"
                create_file = True
                app_namespace = True
        fp.close()

        #create file if it's within our App namespace
        if create_file and app_namespace:
            os.rename(full_file_name, "%s/%s.php" % (stripped_namespace_dir, file_name_to_use))
        #might be a test file to keep. Generate it
        elif test_file:
            if not os.path.exists("./tests/"):
                os.makedirs("./tests/")
            os.rename(full_file_name, "./tests/%s.php" % file_name_to_use)
        #we don't need this garbage. Delete it
        else:
            os.remove(full_file_name)

        i+=1
