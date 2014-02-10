# vagrant needs to be in the login group so it can ssh in with
# our ssh config, and in the admin group so it can passwordless
# sudo, which Vagrant needs it to do.
users:
    vagrant:
        groups: [login, admin]
        require:
          - group: login
          - group: admin

    rapidsms:
        groups: [www-data, login]
        require:
          - group: login
          - group: admin
        public_key:
            - ssh-rsa aaaab3nzac1yc2eaaaabiwaaaqearjyowh2fjexrru0+p3nbeybfwgf/njqzmagz5geybvtst3jzd0btrnwjirngn2bmlycaefbmc6+q33hjcbivvui5/hsmqgcqvwtdh8b8+fpxjrsx9/mwaihrilolqofb1wtg+7g7pd7vhlooq4+phm+9zwlhtxmmcbsuzlzxmjgad8xzopigdpqjwiynnby+hmpthillj8xxjycp+sh2f5vaeyjn/+86l3ojrwdui9ous9rvnpdaznac2rdcqhgk34xlabwivxdu52qmo6saidusqm0h2h0sawbizdlfrer5jro8i8xr28/sfxn2s7vw8xux4+vcz3irmivffplxxw== evanmwheeler@gmail.com
            - ssh-dss AAAAB3NzaC1kc3MAAACBAJRiJzVRJpZqpr+T5oq3wnWNuU5P5WfRnNoVx2N9FrH6ZdzOlQaHrxvKkPSnI0lkhBhxclBuyYj5SNouxFBXzNfRxJO3rtKnnJhc7OsXod0cTojYWHZkHNARnjtLk7D7PGAkdJasdWmqhgFWlJ3MRenigGgsQi4zRn3ga8oCT9k1AAAAFQD6CU1ntmEJAVK4NW+l67s+AATXwQAAAIBfhQWV6b0TRIkJKgFuUwWNrnZ48SBJwWD0gN9BMEOr3NChQRmhU3KX6S2OcOX+VIQ7v8a7y8Izp7w4cojSbaKBCCwAVdwMlbcsMSnWxDWRUxjqIuznkeo8TV/XLPX6fq8BPSctha2lDO0ct9XePRzQZKZPaCyHQif8yA3+ZQF/uQAAAIB581YZ75KG4ltF1oaMB2SQRSyvBrLO/8q6X+RG4PuZvb0IzntBUVTWTSA7PSA4eP4viJxmY+ARTm+bEnk6/5hUaEOI1v0Bf+ZbOWvHLpD7HZ9VX5WCr6QpVD1fDN+vNYw9v73yEZITWALzbEkPHNO8xcU8MJzmcQpHBy/hZoqB6g== ewheeler@curta.local
            - ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAzwmsJrc5AMEOabU3sWXP2WDr937SNZXIfYnA3/L9E0zTewH1O9gpkEVi7EZr4zEbafA9NSkZ5WOemnPTarnLxzjzs1kp25L1/sZPFYaCaJkxA5rQX77UJ7jYab10fwJHkWSr+3DENS9zTzkuJMyv9qB82t0OYK8fawzRp2N2G4ASkH6mkQQplF+8Q20Q74MfSTa3lDSrZxtDYrPlk6FEJOLkk6nE+mSCKl7qhLmjV/tzhgqggLY2f64Lbelp45yM1MTfjU0UwhA18Dq0PSzTTEh4mHhj0B4502uQo2qkBerDPLrpLSOH7arWXaUwKdSZAgJKCKVcVj641X3otpWp7Q== evanmwheeler@gmail.com

    evan:
        groups: [admin, login]
        public_key:
            - ssh-rsa aaaab3nzac1yc2eaaaabiwaaaqearjyowh2fjexrru0+p3nbeybfwgf/njqzmagz5geybvtst3jzd0btrnwjirngn2bmlycaefbmc6+q33hjcbivvui5/hsmqgcqvwtdh8b8+fpxjrsx9/mwaihrilolqofb1wtg+7g7pd7vhlooq4+phm+9zwlhtxmmcbsuzlzxmjgad8xzopigdpqjwiynnby+hmpthillj8xxjycp+sh2f5vaeyjn/+86l3ojrwdui9ous9rvnpdaznac2rdcqhgk34xlabwivxdu52qmo6saidusqm0h2h0sawbizdlfrer5jro8i8xr28/sfxn2s7vw8xux4+vcz3irmivffplxxw== evanmwheeler@gmail.com
            - ssh-dss aaaab3nzac1kc3maaacbajrijzvrjpzqpr+t5oq3wnwnuu5p5wfrnnovx2n9frh6zdzolqahrxvkkpsni0lkhbhxclbuyyj5snouxfbxznfrxjo3rtknnjhc7osxod0ctojywhzkhnarnjtlk7d7pgakdjasdwmqhgfwlj3mrenigggsqi4zrn3ga8oct9k1aaaafqd6cu1ntmejavk4nw+l67s+aatxwqaaaibfhqwv6b0trikjkgfuuwwnrnz48sbjwwd0gn9bmeor3nchqrmhu3kx6s2ocox+viq7v8a7y8izp7w4cojsbakbccwavdwmlbcsmsnwxdwruxjqiuznkeo8tv/xlpx6fq8bpsctha2ldo0ct9xeprzqzkzpacyhqif8ya3+zqf/uqaaaib581yz75kg4ltf1oamb2sqrsyvbrlo/8q6x+rg4puzvb0izntbuvtwtsa7psa4ep4vijxmy+artm+benk6/5huaeoi1v0bf+zbowvhlpd7hz9vx5wcr6qpvd1fdn+vnyw9v73yezitwalzbekphno8xcu8mjzmcqphby/hzoqb6g== ewheeler@curta.local
            - ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAzwmsJrc5AMEOabU3sWXP2WDr937SNZXIfYnA3/L9E0zTewH1O9gpkEVi7EZr4zEbafA9NSkZ5WOemnPTarnLxzjzs1kp25L1/sZPFYaCaJkxA5rQX77UJ7jYab10fwJHkWSr+3DENS9zTzkuJMyv9qB82t0OYK8fawzRp2N2G4ASkH6mkQQplF+8Q20Q74MfSTa3lDSrZxtDYrPlk6FEJOLkk6nE+mSCKl7qhLmjV/tzhgqggLY2f64Lbelp45yM1MTfjU0UwhA18Dq0PSzTTEh4mHhj0B4502uQo2qkBerDPLrpLSOH7arWXaUwKdSZAgJKCKVcVj641X3otpWp7Q== evanmwheeler@gmail.com

    thousand:
        groups: [www-data, admin, login]
        public_key:
            - ssh-rsa aaaab3nzac1yc2eaaaabiwaaaqearjyowh2fjexrru0+p3nbeybfwgf/njqzmagz5geybvtst3jzd0btrnwjirngn2bmlycaefbmc6+q33hjcbivvui5/hsmqgcqvwtdh8b8+fpxjrsx9/mwaihrilolqofb1wtg+7g7pd7vhlooq4+phm+9zwlhtxmmcbsuzlzxmjgad8xzopigdpqjwiynnby+hmpthillj8xxjycp+sh2f5vaeyjn/+86l3ojrwdui9ous9rvnpdaznac2rdcqhgk34xlabwivxdu52qmo6saidusqm0h2h0sawbizdlfrer5jro8i8xr28/sfxn2s7vw8xux4+vcz3irmivffplxxw== evanmwheeler@gmail.com
            - ssh-dss aaaab3nzac1kc3maaacbajrijzvrjpzqpr+t5oq3wnwnuu5p5wfrnnovx2n9frh6zdzolqahrxvkkpsni0lkhbhxclbuyyj5snouxfbxznfrxjo3rtknnjhc7osxod0ctojywhzkhnarnjtlk7d7pgakdjasdwmqhgfwlj3mrenigggsqi4zrn3ga8oct9k1aaaafqd6cu1ntmejavk4nw+l67s+aatxwqaaaibfhqwv6b0trikjkgfuuwwnrnz48sbjwwd0gn9bmeor3nchqrmhu3kx6s2ocox+viq7v8a7y8izp7w4cojsbakbccwavdwmlbcsmsnwxdwruxjqiuznkeo8tv/xlpx6fq8bpsctha2ldo0ct9xeprzqzkzpacyhqif8ya3+zqf/uqaaaib581yz75kg4ltf1oamb2sqrsyvbrlo/8q6x+rg4puzvb0izntbuvtwtsa7psa4ep4vijxmy+artm+benk6/5huaeoi1v0bf+zbowvhlpd7hz9vx5wcr6qpvd1fdn+vnyw9v73yezitwalzbekphno8xcu8mjzmcqphby/hzoqb6g== ewheeler@curta.local
            - ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAzwmsJrc5AMEOabU3sWXP2WDr937SNZXIfYnA3/L9E0zTewH1O9gpkEVi7EZr4zEbafA9NSkZ5WOemnPTarnLxzjzs1kp25L1/sZPFYaCaJkxA5rQX77UJ7jYab10fwJHkWSr+3DENS9zTzkuJMyv9qB82t0OYK8fawzRp2N2G4ASkH6mkQQplF+8Q20Q74MfSTa3lDSrZxtDYrPlk6FEJOLkk6nE+mSCKl7qhLmjV/tzhgqggLY2f64Lbelp45yM1MTfjU0UwhA18Dq0PSzTTEh4mHhj0B4502uQo2qkBerDPLrpLSOH7arWXaUwKdSZAgJKCKVcVj641X3otpWp7Q== evanmwheeler@gmail.com
