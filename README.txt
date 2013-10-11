*** NOTE: THIS IS A SPECIAL ONE/NORTHWEST BRANCH OF TAG CLOUD'S TRUNK SPECIFICALLY FOR WTA.***

Description

    TagCloud is a proof-of-concept product to add a "tag cloud":http://en.wikipedia.org/wiki/Tag_cloud
    made with the keywords of all the items in a Plone site.

    This product is currently being used on the "breaking news site":http://www.jornada.unam.mx/ultimas
    of the mexican diary "La Jornada":http://www.jornada.unam.mx/.

    TagCloud is part of "Julius":http://julius.jornada.com.mx/, a project to
    create a system for Newspaper Workflow Automation based on the
    requirements of La Jornada and on the "IPTC News Architecture":http://www.iptc.org/.

Installation

    This product was tested on Plone 2.5.2.

    Place TagCloud in the Products directory of your Zope instance
    and restart the server. (Linux users should fix permissions of files and folders first.)

    Go to the 'Site Setup' page in the Plone interface and click on the
    'Add/Remove Products' link.

    Choose TagCloud (check its checkbox) and click the 'Install' button.

    You may have to empty your browser cache to see the effects of the
    product installation/uninstallation.

    Uninstall -- This can be done from the same management screen.

How does it works

    TagCloud searchs for all different keywords on 'friendly types' and then
    creates a cloud based on the number of times every single keyword is
    found.

    To define 'friendly types' go to the 'Site Setup' page in the Plone interface
    and click on the 'Search Settings' link; all types used on searches will
    also be used to build the cloud.

    The algorithm to scale the tags and some ideas were taken from Anders
    Pearson's "scaling tag clouds":http://thraxil.com/users/anders/posts/2005/12/13/scaling-tag-clouds/
    blog post.

    Please note that search engine spiders may stress your site if you have a bunch
    of tags, so it's a good idea to add the following lines to your robots.txt file:

        User-Agent: *
        Disallow: /search	# don't do searches

To-do list

    Create a configlet to define TTL of the cache and allow to purge it.

    Limit the items that build the cloud in two different ways:

    * on a given date like 'today' (currently all items are used)

    * to a list of review states (currently only 'published' items are used)

Written by

    Héctor Velarde <hvelarde@jornada.com.mx>
