sys = require 'sys'
exec = require('child_process').exec

finder = (command, args..., callback) ->
  running = "python2 ~/Sandbox/fun-congress/python_congress_finder/congress_finder.py #{command}"
  for a in args
    running += " \"#{a}\""
  exec running, (error, stdout, stderr) ->
    console.log error if error
    callback JSON.parse stdout

exports.finder = finder
