![alt text](https://github.com/rcpch/nhs-hackday-march-25/blob/live/static/scrub-hub-logo.png)

An NHS Hackday project with some remarkable people to build a resource to take the pain out of Oriel, the matching scheme for new doctors looking for their first job.

## To get started

You need to have docker installed

`s/up`

This will create two containers - a django app and a postgres database. On first run it will seed all the boundary files for the geographies.

In the console of the django app then:
`python manage.py seed --mode=all`

then navigate to:
`http://localhost:8008`

## Resources used

- [RCPCH NHS Organisation API](https://rcpch-nhs-organisations.azurewebsites.net/
- https://docs.google.com/document/d/14-RrxIrvWCI2d_yFNtywZkf6IqtSZJNe0aWWBfSjwVk/edit?tab=t.0#heading=h.e75zmv7hdvya)
- https://www.figma.com/proto/cVeSROtwNj1SLKs8Vm0npA/Untitled?node-id=1-394&t=qpVVpIFHNUakAMCI-0&scaling=min-zoom&content-scaling=fixed&page-id=0%3A1