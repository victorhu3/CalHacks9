
console.log("content script ready");


//var full_texts; 
$.get(chrome.runtime.getURL('/modal.html'), function(data) {
    /*$('body').css({
       "z-index" :"-1"
    })*/
    $(data).prependTo('body');
    $('#close_modal_a').on('click', function(event) {
        console.log("close");
        $('#container').hide(); 
    });
});

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
      console.log(sender.tab ?
                  "from a content script:" + sender.tab.url :
                  "from the extension");

        console.log(request);
        
        $("#loader_container").remove();
        $("#suggestions").append("<ol>");
        var arrayLength = request.summary.length;
        for (var i = 0; i < arrayLength; i++) {
            $("#suggestions").append("<li class='suggestion'><a class='nostyle' href='#"+ i + "'>" + request.summary[i] + "</a></li>");
        }
        var full_texts = request.original_reviews;
        $("#suggestions").append("</ol>");
        $('a[href^="#"]').on('click', function(event) {
            var target = $(this).attr('href').substring(1);
            $("#full_review").text(full_texts[parseInt(target)]);
            
            });

        sendResponse({farewell: "goodbye"});
    }
  );