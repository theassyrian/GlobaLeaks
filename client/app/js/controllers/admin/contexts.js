GLClient.controller('AdminContextsCtrl',
  ['$scope', 'AdminContextResource',
  function($scope, AdminContextResource) {
  $scope.admin_receivers_by_id = $scope.Utils.array_to_map($scope.admin.receivers);

  $scope.save_context = function (context, cb) {
    if (context.additional_questionnaire_id == null) {
      context.additional_questionnaire_id = '';
    }

    var updated_context = new AdminContextResource(context);

    return $scope.Utils.update(updated_context, cb);
  };

  $scope.showAddContext = false;
  $scope.toggleAddContext = function() {
    $scope.showAddContext = !$scope.showAddContext;
  };

  $scope.moveUpAndSave = function(elem) {
    $scope.Utils.moveUp(elem);
    $scope.save_context(elem);
  };

  $scope.moveDownAndSave = function(elem) {
    $scope.Utils.moveDown(elem);
    $scope.save_context(elem);
  };
}]).
controller('AdminContextEditorCtrl', ['$scope', '$rootScope', '$http', 'AdminContextResource',
  function($scope, $rootScope, $http, AdminContextResource) {
  $scope.editing = false;

  $scope.toggleEditing = function () {
    $scope.editing = !$scope.editing;
  };

  $scope.moveUp = function(e, idx) { swap(e, idx, -1); };
  $scope.moveDown = function(e, idx) { swap(e, idx, 1); };

  function swap($event, index, n) {
    $event.stopPropagation();

    var target = index + n;
    if (target < 0 || target >= $scope.admin.contexts.length) {
      return;
    }

    $scope.admin.contexts[index] = $scope.admin.contexts[target];
    $scope.admin.contexts[target] = $scope.context;

    $http({
      method: 'PUT',
      url: '/admin/contexts',
      data: {
        'operation': 'order_elements',
        'args': {'ids': $scope.admin.contexts.map(function(c) { return c.id; })},
      },
    }).then(function() {
      $rootScope.successes.push({});
    });
  }

  $scope.showSelect = false;
  $scope.toggleSelect = function() {
    $scope.showSelect = true;
  };

  $scope.toggle = function(receiver) {
    var idx = $scope.context.receivers.indexOf(receiver.id);
    if (idx === -1) {
      $scope.context.receivers.push(receiver.id);
    } else {
      $scope.context.receivers.splice(idx, 1);
    }

    $scope.editContext.$dirty = true;
    $scope.editContext.$pristine = false;
  };

  $scope.moveReceiver = function(rec) {
    $scope.context.receivers.push(rec.id);
    $scope.showSelect = false;
  };

  $scope.receiverNotSelectedFilter = function(item) {
    return $scope.context.receivers.indexOf(item.id) == -1;
  };

  $scope.updateContextImgUrl = function() {
    $scope.contextImgUrl = '/admin/contexts/' + $scope.context.id + '/img#' + $scope.Utils.randomFluff();
  };

  $scope.updateContextImgUrl();

  $scope.deleteContext = function() {
    $scope.Utils.deleteDialog($scope.context).then(function() {
      return $scope.Utils.deleteResource(AdminContextResource, $scope.admin.contexts, $scope.context);
    });
  };
}]).
controller('AdminContextReceiverSelectorCtrl', ['$scope', function($scope) {
  $scope.moveUp = function(idx) { swap(idx, -1); };
  $scope.moveDown = function(idx) { swap(idx, 1); };

  function swap(index, n) {
    var target = index + n;
    if (target > -1 && target < $scope.context.receivers.length) {
      var tmp = $scope.context.receivers[target];
      var tmpIdx = $scope.context.receivers[index];
      $scope.context.receivers[target] = tmpIdx;
      $scope.context.receivers[index] = tmp;
    }
  }
}]).
controller('AdminContextAddCtrl', ['$scope', function($scope) {
  $scope.new_context = {};

  $scope.add_context = function() {
    var context = new $scope.AdminUtils.new_context();

    context.name = $scope.new_context.name;
    context.questionnaire_id = $scope.admin.node.default_questionnaire;
    context.presentation_order = $scope.newItemOrder($scope.admin.contexts, 'presentation_order');

    context.$save(function(new_context){
      $scope.admin.contexts.push(new_context);
      $scope.new_context = {};
    });
  };
}]);
