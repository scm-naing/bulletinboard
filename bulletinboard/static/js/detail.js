function goToPostDetail(post) {
  $.ajax({
    type: 'GET',
    url: "/post/detail",
    data: {
      'post_id': post
    },
    success: function (response) {
      const data = JSON.parse(response);
      let status = data.fields.status === "1" ? 'Active' : 'Not Active';
      $("#title").html(data.fields.title);
      $("#description").html(data.fields.description);
      $("#status").html(status);
      $("#created_date").html(data.fields.created_at);
      $("#created_user").html(data.created_user_name);
      $("#updated_date").html(data.fields.updated_at);
      $("#updated_user").html(data.updated_user_name);
    },
    error: function (response) {
      alert(response["responseJSON"]["error"]);
    }
  })
}

function goToUserDetail(user) {
  $.ajax({
    type: 'GET',
    url: "/user/detail",
    data: {
      'user_id': user
    },
    success: function (response) {
      const data = JSON.parse(response);
      let type = data.fields.type === "0" ? 'Admin' : 'User';
      if (data.fields.profile) $('#user-detail-profile').html("<img src='/static/" + data.fields.profile + "' alt=user profile' class='profile-img'>")
      else $('#user-detail-profile').html("<p class='glyphicon glyphicon-user profile-icon'></p>")
      $("#user-name").html(data.fields.name);
      $("#user-type").html(type);
      $("#user-email").html(data.fields.email);
      $("#user-phone").html(data.fields.phone);
      $("#user-dob").html(data.fields.dob);
      $("#user-address").html(data.fields.address);
      $("#created_date").html(data.fields.created_at);
      $("#created_user").html(data.created_user_name);
      $("#updated_date").html(data.fields.updated_at);
      $("#updated_user").html(data.updated_user_name);
    },
    error: function (response) {
      alert(response["responseJSON"]["error"]);
    }
  })
}

function goToPostDelete(post) {
  $.ajax({
    type: 'GET',
    url: "/post/delete/confirm",
    data: {
      'post_id': post
    },
    success: function (response) {
      const data = JSON.parse(response);
      let status = data.fields.status === "1" ? 'Active' : 'Not Active';
      $("#post-delete-id").html(post);
      $("#post-delete-title").html(data.fields.title);
      $("#post-delete-description").html(data.fields.description);
      $("#post-delete-status").html(status);
    },
    error: function (response) {
      alert(response["responseJSON"]["error"]);
    }
  })
}

function postDelete() {
  const id = $("#post-delete-id").html();
  $.ajax({
    type: 'GET',
    url: "/post/delete",
    data: {
      'post_id': id
    },
    success: function () {
      $("#detailDelModal").modal('hide');
      location.reload(true);
    },
    error: function (response) {
      alert(response["responseJSON"]["error"]);
    }
  })
}

function goToUserDelete(post) {
  $.ajax({
    type: 'GET',
    url: "/user/delete/confirm",
    data: {
      'user_id': post
    },
    success: function (response) {
      const data = JSON.parse(response);
      let type = data.fields.type === "0" ? 'Admin' : 'User';
      $("#user-delete-id").html(post);
      $("#user-delete-name").html(data.fields.name);
      $("#user-delete-type").html(type);
      $("#user-delete-email").html(data.fields.email);
      $("#user-delete-phone").html(data.fields.phone);
      $("#user-delete-dob").html(data.fields.dob);
      $("#user-delete-address").html(data.fields.address);
    },
    error: function (response) {
      alert(response["responseJSON"]["error"]);
    }
  })
}

function userDelete() {
  const id = $("#user-delete-id").html();
  $.ajax({
    type: 'GET',
    url: "/user/delete",
    data: {
      'user_id': id
    },
    success: function () {
      $("#userDelModal").modal('hide');
      location.reload(true);
    },
    error: function (response) {
      alert(response["responseJSON"]["error"]);
    }
  })
}

function downloadCSV(postList) {
  $.ajax({
    type: 'GET',
    url: "/post/list/download",
    data: {},
    success: function (response) {
      let hiddenElement = document.createElement('a');
      const today = new Date();
      const date = today.getFullYear().toString() + (today.getMonth() + 1).toString() + today.getDate().toString() +
        today.getHours().toString() + today.getMinutes().toString() + today.getSeconds().toString();
      hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(response);
      hiddenElement.target = '_blank';
      hiddenElement.download = 'post_list' + date + '_' + '.csv';
      hiddenElement.click();
    },
    error: function (response) {
      alert(response["responseJSON"]["error"]);
    }
  })
}