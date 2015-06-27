sys = require 'sys'
exec = require('child_process').exec

congress = (command, args...) ->
  running = "python2 ./congress_finder.py #{command}"
  for a in args
    running += " "
    running += a
  exec running, (error, stdout, stderr) ->
    console.log error if error
    return JSON.parse stdout

congress "getAllReps"
