/*
 * Bootstrap Image Gallery JS Example 1.0
 * https://github.com/blueimp/Bootstrap-Image-Gallery
 *
 * Copyright 2012, Sebastian Tschan
 * https://blueimp.net
 *
 * Licensed under the MIT license:
 * http://www.opensource.org/licenses/MIT
 */

/*jslint unparam: true */
/*global window, document, $ */

$(function () {
    'use strict';

    // Start slideshow button:
    $('#start-slideshow').button().click(function () {
        var options = $(this).data(),
            modal = $(options.target),
            data = modal.data('modal');
        if (data) {
            $.extend(data.options, options);
        } else {
            options = $.extend(modal.data(), options);
        }
        modal.find('.modal-slideshow').find('i')
            .removeClass('icon-play')
            .addClass('icon-pause');
        modal.modal(options);
    });

    // Toggle fullscreen button:
    $('#toggle-fullscreen').button().click(function () {
        var button = $(this),
            root = document.documentElement;
        if (!button.hasClass('active')) {
            $('#modal-gallery').addClass('modal-fullscreen');
            if (root.webkitRequestFullScreen) {
                root.webkitRequestFullScreen(
                    window.Element.ALLOW_KEYBOARD_INPUT
                );
            } else if (root.mozRequestFullScreen) {
                root.mozRequestFullScreen();
            }
        } else {
            $('#modal-gallery').removeClass('modal-fullscreen');
            (document.webkitCancelFullScreen ||
                document.mozCancelFullScreen ||
                $.noop).apply(document);
        }
    });

    // Load images via flickr for demonstration purposes:
    $('#moreImages').button().click( function() {
	     var url =  'http://localhost:8000/moreImages';
	     $.getJSON(url, null, function (data) {
	        var photoUrl;
	        var urlSmall;
	        var gallery = $('#gallery'),url;
	        $.each(data, function (index, photo) {
	   	    	photoUrl = 'http://tube.liorkirsch.webfactional.com/changeImage?url=' + photo.url;
		    	urlSmall = photoUrl + '&height=150';
	            $('<a rel="gallery"/>')
	                .append($('<img>').prop('src', urlSmall)
	                .prop('onerror','this.parentNode.parentNode.removeChild(this.parentNode)')
	                )
	                .prop('href', photoUrl)
	                .prop('title', photo.title)
	                .appendTo(gallery);
	        });
	    });
	});
});

$(window).load(function(){
	$('#moreImageDiv').show();
});
