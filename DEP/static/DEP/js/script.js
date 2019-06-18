"use strict";

$(document).ready(function() {
    $(".modular_btn").click(function(event){

        $.ajax({
            type: "POST",
            url: "/modular",
            async: true,
            data: {
                'csrfmiddlewaretoken': $("[name=csrfmiddlewaretoken]").val(),
                'method': $(this).attr("id")
            },
            success: function(response) {
//                $("#modal_other").css( "maxWidth", ( $( window ).width() * 0.9 | 0 ) + "px" );
//                $('#modal_other').find('.modal_other_text').text(response['output']);
//                $("#modal_other").modal({
//                    closeExisting: false
//                });
            },
            error: function(response) {
//                $("#modal_other").css( "maxWidth", ( $( window ).width() * 0.9 | 0 ) + "px" );
//                $('#modal_other').find('.modal_other_text').text(response['output']);
//                $("#modal_other").modal({
//                    closeExisting: false
//                });
            }
        });
    });

    $("#apply_button").click(function(e){
        $.ajax({
            type: "POST",
            url: "/apply",
            async: true,
            data: {
                'csrfmiddlewaretoken': $("[name=csrfmiddlewaretoken]").val()
            },
            success: function(response) {
               

                if (response['result'] == 'Success') {
                    $('#exampleModalApply').find('.text_apply').html("<span class='fa fa-check fa-3x checkicon'></span>");
                    $('#exampleModalApply').find('.text_apply2').text("Success");
                } else if(response['result'] == 'Error'){
                    $('#exampleModalApply').find('.text_apply').html("<span class='fa fa-exclamation fa-3x exclamationicon'></span>");
                    $('#exampleModalApply').find('.text_apply2').text(response['details']);
                } else if(response['result'] == 'Questionable') {
                    $('#exampleModalApply').find('.text_apply').html("<span class='fa fa-question fa-3x questionicon'></span>");
                    $('#exampleModalApply').find('.text_apply2').text(response['details']);
                } else {
                    $('#exampleModalApply').find('.text_apply').html("<span class='fa fa-question fa-3x questionicon'></span>");
                    $('#exampleModalApply').find('.text_apply2').text(response['details']);
                }

                
            },
            error: function(response) {
                $('#exampleModalApply').find('.modal_status_text').text('Error');
                $('#exampleModalApply').find('.modal_output_text').text('Likely connection issues or bad server response');
                $('#exampleModalApply').find('.modal_additional_text').text('');
                $('#exampleModalApply').find('.graphic_result').html("<span class='fa fa-exclamation fa-3x exclamationicon'></span>");
                $("#exampleModalApply").modal({
                    closeExisting: false
                });

            }
        });
    });

    $("#add_button").click(function(e){
        $.ajax({
            type: "POST",
            url: "/add",
            async: true,
            data: {
                'id': $('#serial_number')[0].value,
                'csrfmiddlewaretoken': $("[name=csrfmiddlewaretoken]").val()
            },
            success: function(response) {
                $('#exampleModal2').find('.test_test2').html("<span class='fa fa-check fa-3x checkicon'></span>");

                if (response['result'] == 'Success') {
                    $('#exampleModal2').find('.text_add').html("<span class='fa fa-check fa-3x checkicon'></span>");
                    $('#exampleModal2').find('.text_add2').text("Success");
                } else if(response['result'] == 'Error'){
                    $('#exampleModal2').find('.text_add').html("<span class='fa fa-exclamation fa-3x exclamationicon'></span>");
                    $('#exampleModal2').find('.text_add2').text(response['details']);
                } else if(response['result'] == 'Questionable') {
                    $('#exampleModal2').find('.text_add').html("<span class='fa fa-exclamation fa-3x exclamationicon'></span>");
                    $('#exampleModal2').find('.text_add2').text(response['details']);
                } else {
                    $('#exampleModal2').find('.text_add').html("<span class='fa fa-exclamation fa-3x exclamationicon'></span>");
                }
            },
            error: function(response) {
             $('#exampleModal2').find('.text_add').html("<span class='fa fa-exclamation fa-3x exclamationicon'></span>");
            }
        });
    });

    $("#remove_button").click(function(e){
        $.ajax({
            type: "POST",
            url: "/remove",
            async: true,
            data: {
                'id': $('#serial_number')[0].value,
                'csrfmiddlewaretoken': $("[name=csrfmiddlewaretoken]").val()
            },
            success: function(response) {
                
                    $('#exampleModal').find('.test_test').html("<span class='fa fa-check fa-3x checkicon'></span>");

                if (response['result'] == 'Success') {
                    $('#exampleModal').find('.text_remove').html("<span class='fa fa-check fa-3x checkicon'></span>");
                    $('#exampleModal').find('.text_remove2').text("Device removed");
                } else if(response['result'] == 'Error'){
                    $('#exampleModal').find('.text_remove').html("<span class='fa fa-exclamation fa-3x exclamationicon'></span>");
                    $('#exampleModal').find('.text_remove2').text("Device not found");
                } else if(response['result'] == 'Questionable') {
                    $('#exampleModal').find('.text_remove').html("<span class='fa fa-exclamation fa-3x exclamationicon'></span>");
                    $('#exampleModal').find('.text_remove2').text("Device not found");
                } else {
                    $('#exampleModal').find('.text_remove').html("<span class='fa fa-exclamation fa-3x exclamationicon'></span>");
                    $('#exampleModal').find('.text_remove2').text("Device not found");
                }

            },
            error: function(response) {
                    $('#exampleModal').find('.text_remove').html("<span class='fa fa-exclamation fa-3x exclamationicon'></span>");
            }
        });
    });

    $("#get_json_form").submit(function(event) {
        event.preventDefault();
        $.ajax({
            type: "GET",
            url: "/get_json",
            async: true,
            success: function(response) {
                $('#modal_json').find('.modal_json_text').text(JSON.stringify(response, undefined, 2));
                $("#modal_json").modal({
                    closeExisting: false
                });
            },
            error: function(response) {
                $('#modal_json').find('.modal_json_text').text('Error');
                $("#modal_json").modal({
                    closeExisting: false
                });
            }
        });
    });
});
