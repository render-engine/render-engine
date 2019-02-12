import config
import arrow 

from pages.blog import BlogPost
from pages.page import get_ct_time

class MicroBlogPost(BlogPost):
    title = ''
    def __init__(self, base_file, output_path):
        super().__init__(base_file=base_file, output_path=output_path)
        self.date_published = self.get_date_published()
    
    
    def get_date_published(self):
        """Returns the value of _date_published or _date, or created_datetime from
the system if not defined. NOTE THE SYSTEM DATE IS KNOWN TO CAUSE
ISSUES WITH FILES THAT WERE COPIED OR TRANSFERRED WITHOUT THEIR
METADATA BEING TRANSFER READ AS WELL"""

        if self._date_published:
            date = arrow.get(self._date_published, config.TIME_FORMAT)

        elif self._date:
            date = arrow.get(self._date, config.TIME_FORMAT)

        elif self.base_file:
            try: 
                date = arrow.get(self.base_file.stem, 'YYYYMMDDHHmm')
                    
            except:
                date = get_ct_time(self.base_file)

        else:
             date = get_ct_time(self.base_file)

        return date.format(config.TIME_FORMAT)
