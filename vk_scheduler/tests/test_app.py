import unittest


class TestModels(unittest.TestCase):
    def setUp(self):
        self.raw_post = dict(
            id=133, from_id=-130286321, owner_id=-130286321, date=1476648041, marked_as_ads=0,
            post_type='post', text='''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce vel elit congue, tempus velit nec, viverra leo. Sed pulvinar aliquet consequat. Sed in nunc turpis. Suspendisse molestie nisi sed rhoncus molestie. Morbi id tortor ut urna viverra volutpat at a sapien. Fusce ac odio et dui varius sagittis. Aliquam tempus sollicitudin leo, non dictum massa ullamcorper id. Mauris non enim at orci vehicula tristique vitae sollicitudin odio. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Integer tincidunt eleifend tellus et accumsan. Curabitur pellentesque aliquet sapien. Suspendisse egestas feugiat congue. Sed id pharetra massa. Fusce vitae aliquam mi. Sed aliquet, nibh eget vehicula cursus, mauris neque porttitor lectus, in aliquam arcu arcu in ex.

Donec dapibus justo nec purus euismod, nec accumsan lorem maximus. Phasellus et sem quam. Nunc ipsum sapien, malesuada id velit pellentesque, mollis pellentesque est. Morbi elementum sagittis vulputate. Cras ipsum justo, facilisis ac vulputate nec, sollicitudin vel neque. Curabitur varius consequat neque sit amet laoreet. Suspendisse eget fermentum felis, eu venenatis augue. Nullam et eros quis justo rhoncus molestie. Interdum et malesuada fames ac ante ipsum primis in faucibus. In ultricies feugiat massa, eget iaculis diam consequat a. Fusce ut eros id massa fermentum venenatis. Nam nisl ipsum, consequat vitae mollis et, scelerisque ac arcu. Sed a sem semper lorem congue iaculis. Curabitur imperdiet magna a lectus dignissim tristique. Nunc condimentum libero blandit bibendum pellentesque.

Quisque eu tellus eget odio vulputate aliquet. In ac justo at nisi tempor pretium id sollicitudin leo. Phasellus venenatis magna non urna ultricies placerat. Fusce eget interdum ligula. Sed turpis turpis, commodo non urna vel, congue ultrices dui. Nullam ut tristique purus, et facilisis diam. Vestibulum ultrices, velit et convallis semper, diam mi luctus massa, ac cursus mi mauris quis augue. Nam fringilla egestas fermentum. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Aliquam iaculis consectetur convallis.

Fusce porta felis sit amet hendrerit laoreet. Praesent ipsum lorem, iaculis ut vehicula eu, aliquet quis est. Integer non est justo. Vestibulum auctor consequat ex, vitae consectetur diam porta sit amet. Nulla pretium fermentum velit, ac consectetur purus ultricies quis. Curabitur vitae velit nec metus vulputate iaculis et ac turpis. Curabitur quam leo, interdum et urna eget, blandit finibus diam. Sed ex nunc, tincidunt eu justo a, tempus lobortis felis. Mauris maximus augue massa. Etiam tristique ligula turpis, id facilisis turpis mattis sit amet. Etiam vehicula mauris in lacus tincidunt, quis convallis ipsum condimentum. Nam facilisis porta dui at consectetur. Etiam eget dui nulla. Proin ac consequat nulla. Cras vel nisi nec purus pretium commodo sit amet sed ex. Nulla facilisi.

Sed et est sit amet dui bibendum vulputate id vel enim. Nam pharetra blandit metus. Aenean aliquam et eros tempus posuere. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque vitae ullamcorper enim. Maecenas neque ex, facilisis vel arcu quis, varius posuere est. Proin blandit, justo quis convallis lacinia, odio libero tincidunt velit, rhoncus gravida tortor mauris id sapien. Cras non ex purus. Sed pharetra turpis sit amet elit placerat tincidunt.

https://vk.com/durov?z=photo1_376599151%2Falbum1_0%2Frev
https://vk.com/durov?z=album1_136592355
https://vk.com/durov?z=video1708231_171383594%2Fvideos1%2Fpl_1_-2
https://www.youtube.com/watch?v=WLROFAYH6-4
https://vimeo.com/13525706
https://vk.com/album95860840_228526067
https://www.youtube.com/watch?v=kYfNvmF0Bqw
https://vk.com/durov?z=photo11316927_428929212%2Fwall1_1237616
https://pp.vk.me/c7003/v7003978/1ed9/yoeGXOWmW-M.jpg
https://vk.com/durov?z=photo1_326652857%2Fphotos1''',
            can_edit=1, created_by=33151248, can_delete=1, can_pin=1,
            attachments=[
                dict(
                    type='photo',
                    photo={
                        'id': 312177624,
                        'album_id': 136592355,
                        'owner_id': 1,
                        'photo_75': 'https://cs7050.vk...847/TheKsCcSV0A.jpg',
                        'photo_130': 'https://cs7050.vk...848/n8L9XeNpicE.jpg',
                        'photo_604': 'https://cs7050.vk...849/Mc63nZlMkyw.jpg',
                        'photo_807': 'https://cs7050.vk...84a/-zTV-Vf4ibY.jpg',
                        'photo_1280': 'https://cs7050.vk...84b/49OlZbdrjsk.jpg',
                        'photo_2560': 'https://cs7050.vk...84c/65oW_-qobmE.jpg',
                        'width': 1920,
                        'height': 1080,
                        'text': '',
                        'date': 1380289479,
                        'access_key': '78953eef7502b0f0fc'
                    }
                )
            ],
            post_source={'type': 'vk'},
            comments={
                'count': 0,
                'can_post': 1
            },
            likes={
                'count': 0,
                'user_likes': 0,
                'can_like': 1,
                'can_publish': 1
            },
            reposts={
                'count': 0,
                'user_reposted': 0
            }
        )
