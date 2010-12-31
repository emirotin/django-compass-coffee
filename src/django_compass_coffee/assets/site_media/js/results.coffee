$ ->
  $('#results .res .gauge').each ->
    gauge = $ this
    gauge.wrap '<div class="gauge-wrapper" />'
    votes = gauge.parent().siblings '.votes'
    gauge.animate {width: gauge.attr('_width') + '%'}, 1000, ->
      votes.css "visibility", "visible"