import pkg_resources
import uuid

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
from xblock.fragment import Fragment


class DashXBlock(XBlock):

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    count = Integer(default=0, scope=Scope.user_state, help="A simple counter, to show something happening")
    width = String(default="700", scope=Scope.settings, help="The width of the generated svg")
    height = String(default="300", scope=Scope.settings, help="The height of the generated svg")
    groupBy = String(default="actor.mbox", scope=Scope.settings, help="The xAPI xpath used to group statements by")
    display_name = String(display_name="Display Name", default="xAPI Dashboard", scope=Scope.settings, help="Name of the component in the edxplatform")
                              
    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the DashXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/dashxblock.html")
        frag = Fragment(html.format(self=self))
        
        frag.add_css(self.resource_string("static/css/dashxblock.css"))
        frag.add_css(self.resource_string("static/css/nv.d3.css"))
        
        frag.add_javascript(self.resource_string("static/js/xapicollection.js"))
        frag.add_javascript(self.resource_string("static/js/xapidashboard.js"))
        frag.add_javascript(self.resource_string("static/js/src/dashxblock.js"))
        
        frag.initialize_js('DashXBlock')
        return frag

    # TO-DO: change this view to display your data your own way.
    def studio_view(self, context=None):
        html = self.resource_string("static/html/dashxblock_edit.html")
        frag = Fragment(html.format(self=self))
        
        frag.initialize_js('DashXBlock')
        return frag

    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def increment_count(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        # Just to show data coming in...
        assert data['hello'] == 'world'

        self.count += 1
        return {"count": self.count}
        
    @XBlock.json_handler
    def update_dashboard(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        # Just to show data coming in...
        
        self.display_name = data['display_name']
        self.height = data['height']
        self.width = data['width']
        
        print "This is the incoming data:"
        print data

        return {"success": self.height}

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("DashXBlock",
             """<vertical_demo>
                <dashxblock width="1000" height="600"/>
                <dashxblock width="300" height="100" groupBy="verb.display.en-US"/>
                </vertical_demo>
             """),
        ]
