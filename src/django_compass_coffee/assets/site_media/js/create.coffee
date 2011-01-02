h = Haml.render
new_ans_tmpl = Haml '%input{type: "text", name: "#{name}"}'
$ ->
  total_answers = 3
  add_answer = ->
    if this.name != 'answer_' + total_answers
      return
    total_answers++;
    $('#answers').append h '%br'
    a = $ h new_ans_tmpl {'name': "answer_" + total_answers}
    $('#answers').append a
    a.focus add_answer
    $('#total_answers').attr "value", total_answers
    return #cheating JavaScript Lint
  $('#answers > input').focus add_answer
