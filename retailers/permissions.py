from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		# Read-only permissions are allowed for any request
		if request.method in permissions.SAFE_METHODS:
			return True
			# Write permissions are only allowed to admin users
		if request.user.role == 2:
			return True
		#return 2 == request.user.role