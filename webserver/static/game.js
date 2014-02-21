(function () {

  $(function () {
    var connection = new SockJS('http://' + window.location.host + '/socket');

    connection.onopen = function (ev) {
      console.log('opened', ev);
    };

    connection.onclose = function (ev) {
      console.log('closed', ev);
    };

    connection.onmessage = function (ev) {
      console.log('message', ev.data);
      navigator.vibrate([200, 200, 200]);
      $data.append("<p><strong>received:</strong> " + ev.data.message + "</p>");
    };

    connection.onerror = function (ev) {
      console.log('error', ev);
    };

    window.connection = connection;

    var $data = $("#data"),
        $input = $("input:first");

    $input.on("keypress", function (ev) {
      if (ev.keyCode === 13) {
        ev.preventDefault();
        connection.send($input.val());
        $data.append("<p><strong>send:</strong> " + $input.val() + "</p>");
        $input.val('');
      }
    });
  });

}());
