$(function(){
	var showOption;
	if(showOption === 'True' || showOption === undefined){
		$('#rform').addClass('hide');
		$('#lform').removeClass('hide');
	}else {
		$('#lform').addClass('hide');
		$('#rform').removeClass('hide');
	}
	$('.switch').on('click', function(){
		$('.switch, .lrforms').toggleClass('hide');
	})
	$('form').on('submit', function(){
		showOption = $('.hidden').val();
		return showOption;
	})
	var password;
	$('#pw').on('focusout', function(){
		password = $(this).val();
		return password;
	})
	$('#pwConf').on('keyup', function(){
		var pwConf = $(this).val();
		if(pwConf !== password){
			$(this).css('color','red');
			$('.regBtn').prop('disabled', true);
		}else {
			$(this).css('color','black');
			$('.regBtn').removeAttr('disabled');
		}
	})
})