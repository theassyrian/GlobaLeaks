GLClient.controller('AdminFieldEditorCtrl', ['$scope', '$uibModal',
  function($scope, $uibModal) {
    $scope.editing = false;
    $scope.new_field = {};

    if ($scope.children) {
      $scope.fields = $scope.children;
    }

    $scope.children = $scope.field.children;

    $scope.toggleEditing = function () {
      $scope.editing = !$scope.editing;
    };

    $scope.isMarkableSubjectToStats = function(field) {
      return (['inputbox', 'textarea', 'fieldgroup'].indexOf(field.type) === -1);
    };

    $scope.isMarkableSubjectToPreview = function(field) {
      return (['fieldgroup', 'fileupload'].indexOf(field.type) === -1);
    };

    $scope.typeSwitch = function (type) {
      if (['inputbox', 'textarea'].indexOf(type) !== -1) {
        return 'inputbox_or_textarea';
      }

      if (['checkbox', 'selectbox', 'multichoice'].indexOf(type) !== -1) {
        return 'checkbox_selectbox_multichoice';
      }

      return type;
    };

    $scope.showConfiguration = function(field) {
      if (['inputbox', 'textarea', 'checkbox', 'multichoice', 'selectbox', 'tos', 'date'].indexOf(field.type) > -1) {
        return true;
      }

      if (field.instance === 'template' && (['whistleblower_identity'].indexOf(field.id) > -1)) {
        return true;
      }

      return false;
    };

    $scope.showOptions = function(field) {
      if (['checkbox', 'selectbox', 'multichoice'].indexOf(field.type) > -1) {
        return true;
      }

      return false;
    };

    $scope.delField = function(field) {
      $scope.deleted_fields_ids.push(field.id);
      return $scope.Utils.deleteResource($scope.fieldResource, $scope.fields, field);
    };

    $scope.showAddQuestion = $scope.showAddQuestionFromTemplate = false;
    $scope.toggleAddQuestion = function() {
      $scope.showAddQuestion = !$scope.showAddQuestion;
      $scope.showAddQuestionFromTemplate = false;
    };

    $scope.toggleAddQuestionFromTemplate = function() {
      $scope.showAddQuestionFromTemplate = !$scope.showAddQuestionFromTemplate;
      $scope.showAddQuestion = false;
    };

    $scope.addOption = function () {
      var new_option = {
        'id': '',
        'label': '',
        'score_points': 0,
        'trigger_field': ''
      };

      new_option.presentation_order = $scope.newItemOrder($scope.field.options, 'presentation_order');

      $scope.field.options.push(new_option);
    };

    $scope.moveOptionUp = function(idx) { swapOption(idx, -1); };
    $scope.moveOptionDown = function(idx) { swapOption(idx, 1); };

    function swapOption(index, n) {
      var target = index + n;
      if (target < 0 || target >= $scope.field.options.length) {
        return;
      }
      var a = $scope.field.options[target];
      var b = $scope.field.options[index];
      $scope.field.options[target] = b;
      $scope.field.options[index] = a;
    }

    $scope.delOption = function(option) {
      $scope.field.options.splice($scope.field.options.indexOf(option), 1);
    };

    $scope.save_field = function(field) {
      var updated_field;

      field.options.forEach(function(option) {
        if ($scope.deleted_fields_ids.indexOf(option.trigger_field) !== -1) {
          option.trigger_field = '';
        }
      });

      $scope.Utils.assignUniqueOrderIndex(field.options);

      updated_field = new $scope.fieldResource(field);

      $scope.Utils.update(updated_field);
    };

    $scope.moveUpAndSave = function(elem) {
      $scope.Utils.moveUp(elem);
      $scope.save_field(elem);
    };

    $scope.moveDownAndSave = function(elem) {
      $scope.Utils.moveDown(elem);
      $scope.save_field(elem);
    };

    $scope.moveLeftAndSave = function(elem) {
      $scope.Utils.moveLeft(elem);
      $scope.save_field(elem);
    };

    $scope.moveRightAndSave = function(elem) {
      $scope.Utils.moveRight(elem);
      $scope.save_field(elem);
    };

    $scope.add_field = function() {
      var field = $scope.AdminUtils.new_field('', $scope.field.id);
      field.label = $scope.new_field.label;
      field.type = $scope.new_field.type;
      field.attrs = $scope.admin.get_field_attrs(field.type);
      field.y = $scope.newItemOrder($scope.field.children, 'y');

      field.instance = $scope.field.instance;

      if (field.type === 'fileupload') {
        field.multi_entry = true;
      }

      field.$save(function(new_field){
        $scope.field.children.push(new_field);
        $scope.new_field = {};
      });
    };

    $scope.add_field_from_template = function() {
      var field = $scope.AdminUtils.new_field('', $scope.field.id);
      field.template_id = $scope.new_field.template_id;
      field.instance = 'reference';
      field.y = $scope.newItemOrder($scope.field.children, 'y');

      field.$save(function(new_field){
        $scope.field.children.push(new_field);
	$scope.new_field = {};
      });
    };

    $scope.fieldIsMarkableSubjectToStats = $scope.isMarkableSubjectToStats($scope.field);
    $scope.fieldIsMarkableSubjectToPreview = $scope.isMarkableSubjectToPreview($scope.field);

    function findParents(field_id, field_lst) {
       for (var i = 0; i < field_lst.length; i++) {
         var field = field_lst[i];
         var pot = [field.id].concat(findParents(field_id, field.children));
         if (pot.indexOf(field_id) > -1) {
            return pot;
         }
       }
       return [];
    }

    $scope.triggerFieldDialog = function(option) {
      var t = [];
      $scope.questionnaire.steps.forEach(function(step) {
        step.children.forEach(function(f) {
          t.push(f);
          t = t.concat(enumerateChildren(f));
        });
      });

      var direct_parents = findParents($scope.field.id, $scope.step.children);
      $scope.all_fields = t.filter(function(f) { return direct_parents.indexOf(f.id) < 0; })

      function enumerateChildren(field) {
        var c = [];
        if (angular.isDefined(field.children)) {
          field.children.forEach(function(field) {
            c.push(field);
            c = c.concat(enumerateChildren(field));
          });
        }
        return c;
      }

      return $scope.Utils.openConfirmableModalDialog('views/partials/trigger_field.html', option, $scope);
    };

    $scope.assignScorePointsDialog = function(option) {
      return $scope.Utils.openConfirmableModalDialog('views/partials/assign_score_points.html', option, $scope);
    };
  }
]).
controller('AdminFieldTemplatesCtrl', ['$scope', 'AdminFieldTemplateResource',
  function($scope, AdminFieldTemplateResource) {
    $scope.fieldResource = AdminFieldTemplateResource;
    $scope.deleted_fields_ids = [];

    $scope.admin.fieldtemplates.$promise.then(function(fields) {
      $scope.fields = fields;
    });
  }
]).
controller('AdminFieldTemplatesAddCtrl', ['$scope',
  function($scope) {
    $scope.new_field = {};

    $scope.add_field = function() {
      var field = $scope.AdminUtils.new_field_template($scope.field ? $scope.field.id : '');
      field.instance = 'template';
      field.label = $scope.new_field.label;
      field.type = $scope.new_field.type;
      field.attrs = $scope.admin.get_field_attrs(field.type);

      field.$save(function(new_field){
        $scope.fields.push(new_field);
        $scope.new_field = {};
      });
    };
  }
]);
