$ ->
  enable_ajax = ->
    $("#player_options_modal form").ajaxForm
      target: "#player_options_modal .modal-body"
      success: enable_ajax

  $("#edit_player_options").click ->
    $("#player_options_modal .modal-body").load "player_options", ->
      $("#player_options_modal").modal()
      enable_ajax()

    false
