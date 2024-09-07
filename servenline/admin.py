from django.contrib import admin
from django.utils.html import format_html
from .models import PictureUpload1, PictureUpload2, PictureUpload3, XcrossPictureUpload, VIPPictureUpload, LotteryResult

# Reusable base admin class for all models with pictures
class PictureUploadBaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_active', 'created_date', 'updated_date', 'image_tag')
    list_filter = ('is_active', 'created_date')
    search_fields = ('id',)
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.picture:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.picture.url)
        return "No Image"

    image_tag.short_description = 'Image Preview'

class LotteryResultAdmin(admin.ModelAdmin):
    list_display = ('date', 'first_prize', 'next_drawn_date', 'result_image_tag')
    list_filter = ('date', 'next_drawn_date')
    search_fields = ('first_prize', 'two_down')
    readonly_fields = ('result_image_tag', 'result_image')  # Add result_image to readonly_fields

    def result_image_tag(self, obj):
        if obj.result_image:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.result_image.url)
        return "No Image"

    result_image_tag.short_description = 'Result Image Preview'

# Register all picture-related models using PictureUploadBaseAdmin
admin.site.register(PictureUpload1, PictureUploadBaseAdmin)
admin.site.register(PictureUpload2, PictureUploadBaseAdmin)
admin.site.register(PictureUpload3, PictureUploadBaseAdmin)
admin.site.register(XcrossPictureUpload, PictureUploadBaseAdmin)
admin.site.register(VIPPictureUpload, PictureUploadBaseAdmin)
admin.site.register(LotteryResult, LotteryResultAdmin)
