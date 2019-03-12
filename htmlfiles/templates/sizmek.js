function call_method_x(sessionId) {
    $.ajax({
        url: "https://adapi.sizmek.com/sas/ads",
        type: "GET",
        contentType: 'application/json',
        data: 'from=0&max=25',
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': sessionId
            'api-key': key,
 },

 success: function (data) {
 console.dir(data.result);
 }
 });
}
