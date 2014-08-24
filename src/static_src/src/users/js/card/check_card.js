document.getElementById('id_card').focus();

$(function () {

    var WallData = (function () {
        var block = $('#wall-data');
        var fio = {
            first_name: 'Имя',
            last_name: 'Фамилия',
            patronymic: 'Отчество'
        };
        var docs = {
            passport: 'Паспорт',
            travel_passport: 'Загран Паспорт',
            drive_license: 'Водительское Удостоверение'
        };
        var get_paragraph = function (name, value) {
            return '<p><strong>' + name + '</strong>: ' + value + '</p>';
        };
        var show = function (user) {
            user = $.parseJSON(user)[0]['fields'];
            var buf = '';
            if (user.photo_url) {
                buf += '<img class="img-thumbnail" src="' + user.photo_url + '" alt="" width="300" height="300" />';
            }
            for (var i in fio) {
                buf += get_paragraph(fio[i], user[i]);
            }
            for (var i in docs) {
                if (user[i]) {
                    buf += get_paragraph(docs[i], user[i]);
                }
            }
            block.html(buf);
        };
        var hide = function () {
            block.html('');
        };
        return {
            show: show,
            hide: hide
        }
    })();

    var ErrObj = (function () {
        var message;
        var block = $('#CheckCardForm').find('#alert-card');
        var show = function (status) {
            if ( typeof(status) === 'number' ) {
                switch (status) {
                    case 404:
                        message = 'Пользователя с такой картой не найдено.';
                        break;
                    default:
                        message = 'Сервер не смог выполнить запрос.';
                }
            } else {
                message = status;
            }
            block.html('<strong>Ошибка!</strong> ' + message);
            block.show();
        };
        var hide = function () {
            block.hide();
        };
        return {
            show: show,
            hide: hide
        }
    })();

    var NextLink = (function () {
        var block = $('#next_link');
        var enable = function (url) {
            block.removeClass('disabled').attr('href', url);
        };
        var disable = function () {
            block.addClass('disabled').attr('href', '#');
        };
        return {
            enable: enable,
            disable: disable
        }
    })();

    var check_card = function (e) {
        var val = $(this).val();
        var form = $('#CheckCardForm');
        ErrObj.hide();
        WallData.hide();
        NextLink.disable();

        if (val.length > 2) {

            $.ajax({
                url: form.attr('action'),
                type: "POST",
                data: form.serialize(),
                beforeSend: function (xhr) {
                    xhr.setRequestHeader("X-CSRFToken", Cookie.getCookie('csrftoken'));
                },
                success: function (data) {
                    if (data.status === 'success') {
                        WallData.show(data.user);
                        NextLink.enable(data.reserve);
                    } else {
                        // TODO: Show error message
                        ErrObj.show(500);
                    }
                },
                error: function (jqXHR) {
                    ErrObj.show(jqXHR.status);
                }
            });
        } else {
            ErrObj.show('Неверный штрих код');
        }
    };

    // запрещаю пользлвателю сабмитить по Enter
    $('#id_card').keypress(function (e) {
        if (e.which == '13') {
            e.preventDefault();
            $('#id_card').blur();
        }
    });
    $('#id_card').on('change', check_card);
});