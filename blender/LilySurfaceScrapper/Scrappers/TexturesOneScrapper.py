# Copyright (c) 2019 Bent Hillerkus

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from .AbstractScrapper import AbstractScrapper
from ..ScrappersManager import ScrappersManager

class TexturesOneScrapper(AbstractScrapper):  
    source_name = "Textures.one"
    home_url = "https://www.textures.one"
    
    # There is probably something rotten about doing it this way, but I couldn't really figure out another way
    source_scrapper_type = None # lovely global state
    source_scrapper = None

    @classmethod
    def findSource(cls, url):
        """Find the original page from where the texture is being distributed via scraping."""
        html = super().fetchHtml(None, url)
        if html is None:
            return None
        
        # Scrape the url
        return html.xpath("//span[@class='goLink']/a")[0].get("href")

    @classmethod
    def canHandleUrl(cls, url):
        """Return true if the URL can be scrapped by this scrapper."""
        if "textures.one/go/?id=" in url: # this is superior to url.startswith(), because it can deal with leaving out "https://" or "www."
            source_url = cls.findSource(url)
            if source_url is not None:
                # Look for a scrapper that can scrape the source page
                for S in ScrappersManager.getScrappersList():
                    if S.canHandleUrl(source_url):
                        cls.source_scrapper_type = S
                        cls.source_scrapper = S("") # I'd love to create this in this classes __init__(), but it gave me headache with scope problems.
                        cls.scrapped_type = cls.source_scrapper_type.scrapped_type # This works
                        return True
        return False

    def fetchVariantList(self, url):
        self.source_scrapper.texture_root = self.texture_root # I'd love to do this just once via the constructor, but again, didn't really get __init__() here to work
        return self.source_scrapper.fetchVariantList(url)

    def fetchVariant(self, variant_index, material_data):
        self.source_scrapper.texture_root = self.texture_root
        return self.source_scrapper.fetchVariant(variant_index, material_data)
