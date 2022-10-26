
// SEARCH INPUT SHOW AND HIDE
$(document).ready(function () {
    $("#search-icon").click(function () {
        $("#search-input").show({ direction: "left" }, 1000);
        $("#search-input").focus();
    });
    $("#search-input").focusout(function () {
        $("#search-input").hide({ direction: "right" }, 1000);
    });
});
