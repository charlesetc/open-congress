sys = require 'sys'
exec = require('child_process').exec

congress = (command, args..., callback) ->
  running = "python2 ./congress_finder.py #{command}"
  for a in args
    running += " "
    running += a
  exec running, (error, stdout, stderr) ->
    console.log error if error
    callback JSON.parse stdout

congress "getAllReps", (object) ->
  console.log JSON.stringify object

