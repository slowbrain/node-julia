import os
import re
import sys
import subprocess


def julia_base_from_which_julia():
   path = "";
   which_julia = subprocess.Popen(["/usr/bin/which","julia"],stdout=subprocess.PIPE).communicate()[0];
   if len(which_julia) > 0:
      real_path = os.path.realpath(which_julia.rstrip(os.linesep))
      if real_path:
         dirname = os.path.dirname(real_path)
         path = os.path.split(dirname)[0]
   return path

def julia_base_from_where_julia():
   path = "";
   DEVNULL = open(os.devnull, 'w')
   where_julia = subprocess.Popen(["where","julia.exe"],stdout=subprocess.PIPE,stderr=DEVNULL).communicate()[0];
   if len(where_julia) > 0:
      real_path = os.path.realpath(where_julia.rstrip(os.linesep))
      if real_path:
         dirname = os.path.dirname(real_path)
         path = os.path.split(dirname)[0]
   return path

def julia_base_from_home_directory():
   home = os.path.expanduser("~")
   julia_dir = os.path.join(home,"julia")
   if os.path.isdir(julia_dir): return julia_dir
   return "";

def julia_base_from_working_directory():
    home = os.path.expanduser("~")
    julia_dir = os.path.join(home,"julia")
    if os.path.isdir(julia_dir): return julia_dir
    return "";

def julia_base_from_home_directory_win():
   home = os.path.expanduser("~")
   search_folder = os.path.join(home, "AppData\Local")
   DEVNULL = open(os.devnull, 'w')
   if os.path.isdir(search_folder):
      where_julia = subprocess.Popen(["where","julia.exe", "/r", search_folder],stdout=subprocess.PIPE,stderr=DEVNULL).communicate()[0];
      julia_dir,filename = os.path.split(where_julia)
      if os.path.isdir(julia_dir): return julia_dir
   return "";

def julia_base_from_applications():
   julia_dir = "/Applications/Julia-0.3.0.app/Contents/Resources/julia/"
   if os.path.isdir(julia_dir): return julia_dir
   return ""

def find_julia_base(platform):
   if platform == "win":
      path = julia_base_from_where_julia()
      if path == "": path = julia_base_from_home_directory_win()
   else:
      path = julia_base_from_which_julia()
      if path == "": path = julia_base_from_home_directory()
      if path == "": path = julia_base_from_working_directory()
      if path == "" and len(sys.argv) > 1 and sys.argv[1] == "mac": path = julia_base_from_applications()
      path = re.sub(" ",r"\ ",path)
   return path

def node_version():
   version = subprocess.Popen(["node","--version"],stdout=subprocess.PIPE).communicate()[0];
   if len(version) > 0:
      version = re.sub(r"^v([0-9]*\.[0-9]*\.)([0-9]*).*$","\g<1>x",version).rstrip(os.linesep)
   return version

def get_nj_lib_define_variable():
   path = os.path.abspath("lib")
   return re.sub(r"\\","\\\\\\\\",path)

def get_julia_lib_define_variable(platform):
   if platform == "win": path = find_julia_base(platform) + "\\lib\\julia"
   else: path = re.sub(r"\\ "," ",find_julia_base(platform)) + "/lib/julia"
   return re.sub(r"\\","\\\\\\\\",path)

if sys.argv[2] == "version": print node_version()
elif sys.argv[2] == "base":
   path = find_julia_base(sys.argv[1])
   if not path == "": print path
elif sys.argv[2] == "nj_lib_define":
   print get_nj_lib_define_variable()
elif sys.argv[2] == "julia_lib_define":
   print get_julia_lib_define_variable(sys.argv[1])
