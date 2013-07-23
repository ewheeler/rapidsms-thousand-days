# vagrant needs to be in the login group so it can ssh in with
# our ssh config, and in the admin group so it can passwordless
# sudo, which Vagrant needs it to do.

users:
    vagrant:
        groups: [login, admin]
    rapidsms:
        groups: [www-data, login]
        public_key:
            - ssh-rsa aaaab3nzac1yc2eaaaabiwaaaqearjyowh2fjexrru0+p3nbeybfwgf/njqzmagz5geybvtst3jzd0btrnwjirngn2bmlycaefbmc6+q33hjcbivvui5/hsmqgcqvwtdh8b8+fpxjrsx9/mwaihrilolqofb1wtg+7g7pd7vhlooq4+phm+9zwlhtxmmcbsuzlzxmjgad8xzopigdpqjwiynnby+hmpthillj8xxjycp+sh2f5vaeyjn/+86l3ojrwdui9ous9rvnpdaznac2rdcqhgk34xlabwivxdu52qmo6saidusqm0h2h0sawbizdlfrer5jro8i8xr28/sfxn2s7vw8xux4+vcz3irmivffplxxw== evanmwheeler@gmail.com
    ewheeler:
        groups: [admin, login]
        public_key:
            - ssh-rsa aaaab3nzac1yc2eaaaabiwaaaqearjyowh2fjexrru0+p3nbeybfwgf/njqzmagz5geybvtst3jzd0btrnwjirngn2bmlycaefbmc6+q33hjcbivvui5/hsmqgcqvwtdh8b8+fpxjrsx9/mwaihrilolqofb1wtg+7g7pd7vhlooq4+phm+9zwlhtxmmcbsuzlzxmjgad8xzopigdpqjwiynnby+hmpthillj8xxjycp+sh2f5vaeyjn/+86l3ojrwdui9ous9rvnpdaznac2rdcqhgk34xlabwivxdu52qmo6saidusqm0h2h0sawbizdlfrer5jro8i8xr28/sfxn2s7vw8xux4+vcz3irmivffplxxw== evanmwheeler@gmail.com

postgres:
    - rapidsms
