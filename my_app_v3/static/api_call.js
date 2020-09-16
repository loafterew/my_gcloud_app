  $(function() {
      $('#output').click(function() {
          $.ajax({
              url : '/serve_prediction?url=' + document.getElementById('url').value,
              success: function(data) {
                  $('#classification_text').html(data['classification_text']);
		$('#probability_text').html(data['probability_text']);
		$('#image_code').html(data['image_code']);          
              }
          });
          this.disabled = true;
      });
  })