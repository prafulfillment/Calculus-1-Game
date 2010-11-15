import pygame, logging, re
from pygame.locals import *
from globalfunctions import *

class Graphics(object):
    """ Contains graphics rendering methods """
    
    glyphdict = {}

    @staticmethod
    @errorlog(0)
    def imgwidth(surface):
        """ Gets the image width for a given surface """
        return surface.get_rect().width
    
    @staticmethod
    @errorlog(0)
    def imgheight(surface):
        """ Gets the image height for a given surface """
        return surface.get_rect().height
    
    @staticmethod
    @errorlog()
    def blit(dest_surface, src_surface, xpos='center', ypos='center'):
        """
        Blits src to dest_surface at (xpos, ypos)
        If xpos or ypos is 'center', it centers the image
        If xpos or ypos is > 0 and < 1, it puts the image at that ratio
        """
        if xpos == 'center':
            xpos = dest_surface.get_rect().width / 2 - src_surface.get_rect().width / 2
        elif xpos > 0 and xpos < 1:
            xpos = dest_surface.get_rect().width * xpos - getimgwidth(src_surface) / 2
        if ypos == 'center':
            ypos = getimgheight(dest_surface) / 2 - getimgheight(src_surface) / 2
        elif ypos > 0 and ypos < 1:
            ypos = getimgheight(dest_surface) * ypos - getimgheight(src_surface) / 2
        dest_surface.blit(src_surface,(xpos,ypos))

    @staticmethod
    @errorlog((0,0,0))
    def darken(color,howmuch=10):
        """ Darkens color by howmuch """
        #print "Darkening",color
        if len(color) == 3:
            (r,g,b) = color
        elif len(color) == 4:
            (r,g,b,a) = color
        r-=howmuch; g-=howmuch; b-=howmuch
        if r<0: r=0
        if g<0: g=0
        if b<0: b=0
        #print "Got",(r,g,b)
        if len(color) == 4:
            return (r,g,b,a)
        else:
            return (r,g,b)
        
    @staticmethod
    @errorlog()
    def radial_gradient(srccol, destcol, (width, height), radius=50, centerpos=(0,0)):
        """
        Draws a radial gradient going from srccol to destcol on a widthxheight surface with the given radius at centerpos
        """
        img = pygame.Surface((width, height)).convert_alpha()
        if len(srccol) == 4 or len(destcol) == 4:
            img = img.convert_alpha()
        else:
            img = img.convert()
        
        if len(srccol) == 3 and len(destcol) == 4:
            srccol.append(255)
        elif len(srccol) == 4 and len(destcol) == 3:
            destcol.append(255)
        
        sarray = pygame.surfarray.pixels3d(img)
        for x in range(width):
            for y in range(height):
                for z in range(len(sarray[x][y])):
                    percent = float(distance((x,y),centerpos)**.5) / radius
                    if percent < 0.0: percent = 0.0
                    if percent > 1.0: percent = 1.0
                    sarray[x][y][z] = (destcol[z] - srccol[z]) * percent + srccol[z]
        return img                
    
    @staticmethod
    @errorlog()
    def linear_gradient(srccol, destcol, (width,height), horizontal=False):
        """
        Creates a linear gradient from srccol to destcol on a widthxheight surface
        Gradient is horizontal if horizontal is True
        """
        img = pygame.Surface((width, height))
        if len(srccol) == 4 or len(destcol) == 4:
            img = img.convert_alpha()
        else:
            img = img.convert()
        
        if len(srccol) == 3 and len(destcol) == 4:
            srccol.append(255)
        elif len(srccol) == 4 and len(destcol) == 3:
            destcol.append(255)
            
        if not horizontal:
            for y in range(height):
                percent = y/float(height)
                if percent < 0.0: percent = 0.0
                if percent > 1.0: percent = 1.0
                color = []
                for z in range(len(srccol)):
                    color.append((destcol[z] - srccol[z]) * percent + srccol[z])
                pygame.draw.line(img, color, (0,y),(width,y))
        else:
            for x in range(width):
                percent = x/float(width)
                if percent < 0.0: percent = 0.0
                if percent > 1.0: percent = 1.0
                color = []
                for z in range(len(srccol)):
                    color.append((destcol[z] - srccol[z]) * percent + srccol[z])
                pygame.draw.line(img, color, (x,0),(x,height))
        return img

    @staticmethod
    @errorlog()
    def getLogoText(size, moveleft=-127, colormain='FFFFFF', colorhighlight='FF0000'):
        """ Returns the text necessary to render the logo """
        return "\\f(" + pakenham + ")\\s("+str(size)+")" + \
               "\\s(150%)\\c(" + colorhighlight + ")\\v(-25%)a\\c(" + colormain + ")mp\\v(-40%)ide\\c(" + colorhighlight + ")a" + \
               "\\s(15%)\\h("+str(moveleft)+")\\v(40%)\\c(" + colorhighlight + ")speak through the streets"
    
    @staticmethod
    @errorlog()
    def renderLogo(size, moveleft=-127, colormain='FFFFFF', colorhighlight='FF0000'):
        """ Returns a surface with the ampidea logo rendered """
        return Graphics.renderText(Graphics.getLogoText(size, moveleft, colormain, colorhighlight), 1)
    
    @staticmethod
    def do_word_wrap(lines, wrapwidth, glyph_dict):#=glyphdict):
        """ A helper function to handle bounds checking for a list of lines """
        def charwidth((c,glyph), glyph_dict):#=glyphdict):
            """ Gets the width for a given character/glyph pair """
            if c != None:
                if type(glyph_dict[glyph]) == pygame.Surface:
                    return getimgwidth(glyph_dict[glyph])
                else:
                    return glyph_dict[glyph][0]
            if glyph.has_key('dx'):
                return glyph['dx']
            return 0
        
        def wrapline(line, glyph_dict):#=glyphdict):
            """ A helper function to handle bounds checking for a single line """
            results = []
            while True:
                w = 0
                for pos,ch in enumerate(line):
                    w += charwidth(ch, glyph_dict)
                
                    # Check for overflow
                    if w > wrapwidth:
                        cutoff = pos
                        break
                else:
                    # If there was no overflow, the width is small
                    # enough -- we're done
                    results.append(line)
                    return results
                    
                splitpos = cutoff
                # Try to split on whitespace characters. If there are none, just
                # split at the edge of the screen for now.
                while splitpos > 0 and (line[splitpos][0] == None or 
                                        (not line[splitpos][0].isspace()
                                        and not line[splitpos][0] == '/')):
                    splitpos -= 1
                if splitpos == 0:
                    splitpos = max(cutoff, 1)
                    
                # Split the substrings, removing any intermediate whitespace
                while splitpos > 0 and (line[splitpos-1][0] == None or line[splitpos-1][0].isspace()):
                    splitpos -= 1
                while splitpos < len(line) and (line[splitpos][0] == None or line[splitpos][0].isspace()):
                    if line[splitpos][0] == None:
                        splitpos += 1
                    else:
                        del line[splitpos]
                results.append(line[:splitpos])
                line = line[splitpos:]
        
        new_lines = []
        for line in lines:
            new_lines += wrapline(line, glyph_dict)
        return new_lines

    # The syntax for a text command: backslash, a single alphanumeric character,
    # then zero or more alphanumeric or whitespace characters in parentheses.
    command_regex = r'\\\w\(.*?\)'
    command_pattern = re.compile(command_regex)
    
    @staticmethod
    #@errorlog()
    # Rendering markup language
    #\f(font_name)   Changes the font to font_name
    #\c(color)       Has to be in hex.  Changes the color
    #\s(size)        Changes the font size to size
    #\h(number)      changes the horizontal offset to number (lasts the rest of the current line)
    #\v(number)      Changes the vertical offset to number (lasts the rest of the text)
    #\l(number)      Changes line spacing
    #\a(r|c|l)       Changes the alignment of text to (l)eft, (c)enter, or (r)ight
    def renderText(text, antialias=1, backgroundcolor=(0,0,0,0), wordwrap=False, wrapwidth=600, getsize=False, glyph_dict=None):
        """
        Renders the given text on a surface with the given backgroundcolor.
        Antialiases is antialias is True
        Wordwraps to wrapwidth if wordwrap is True
        Does not render if getsize is True
        """
        t1 = time.time()
        cur_font_name = os.path.join('data', 'fonts', 'freesansbold.ttf')
        cur_font_size = 36
        cur_font = pygame.font.Font(cur_font_name, cur_font_size)
        cur_color = (0,0,0)
        last_glyph_height = cur_font.get_linesize()
        
        lines = []
        
        #print glyph_dict
        if not glyph_dict:
            #print "Setting to Graphics.glyphdict"
            glyph_dict = Graphics.glyphdict
        elif type(glyph_dict) != dict:
            #print "Setting to empty"
            glyph_dict = {}
        #print glyph_dict
        
        
        for line in text.splitlines():
            pos = 0             # The position in the current line
            saw_char = False    # Whether this line has any characters
            
            # Glyphs is a list that contains the glyphs for all characters that
            # will be rendered, as well as information about geometry changes
            # (horizontal / vertical offsets, line spacing)
            glyphs = []
            for cmd in Graphics.command_pattern.finditer(line):
                # Render all the glyphs up to the start of this command
                for c in line[pos : cmd.start()]:
                    if not glyph_dict.has_key((c, cur_font_name, cur_font_size, cur_color)):
                        glyph_dict[(c, cur_font_name, cur_font_size, cur_color)] = cur_font.render(c, antialias, cur_color).convert_alpha()
                    glyphs += [(c, (c, cur_font_name, cur_font_size, cur_color))]
                
                if cmd.start() > pos:
                    saw_char = True
                    last_glyph_height = getimgheight(glyph_dict[glyphs[-1][1]])

                cmd_text = line[cmd.start() : cmd.end()]
                function = cmd_text[1]
                param = cmd_text[3 : -1]   # This range guaranteed to exist by the regex match
                pos = cmd.end()
                
                # Process the command
                try:
                    if function == 'f':
                        cur_font_name = param
                        cur_font = pygame.font.Font(os.path.join( 'data', 'fonts', cur_font_name ), cur_font_size)
                    elif function == 'c':
                        cur_color = (int(param[0:2],16),
                                     int(param[2:4],16),
                                     int(param[4:6],16))
                    elif function == 'b':
                        cur_font.set_bold(str_to_num(param))
                    elif function == 'i':
                        cur_font.set_italic(str_to_num(param))
                    elif function == 'u':
                        cur_font.set_underline(str_to_num(param))
                    elif function == 's':
                        if param[-1] == '%':
                            cur_font_size = float(param[:-1]) / 100.0 * cur_font_size
                        else:
                            cur_font_size = float(param)
                        cur_font_size = int(round(cur_font_size))
                        cur_font = pygame.font.Font(cur_font_name, cur_font_size)

                    # We've checked all the font attributes. Everything else affects
                    # our geometry computations, so add then to the character stream.
                    elif function == 'a':
                        glyphs.append((None, {'alignment': param}))
                    elif function == 'l':
                        glyphs.append((None, {'line_spacing': float(param)}))
                    elif function == 'h':
                        glyphs.append((None, {'dx': int(param)}))
                    elif function == 'v':
                        if param[-1] == '%':
                            param = str_to_num(param[:-1]) / 100.0 * last_glyph_height
                            dy = param
                        else:
                            dy = str_to_num(param)
                        glyphs.append((None, {'dy': dy}))
                except Exception, e:
                    # Ignore this command, but log the error
                    logging.log("Unexpected exception in text command markup: " + str(e))
                    logging.log("Originating command was '" + cmd_text + "'")
            
            # Render any remaining glyphs
            for c in line[pos:]:
                if not glyph_dict.has_key((c, cur_font_name, cur_font_size, cur_color)):
                    glyph_dict[(c, cur_font_name, cur_font_size, cur_color)] = cur_font.render(c, antialias, cur_color).convert_alpha()
                glyphs += [(c, (c, cur_font_name, cur_font_size, cur_color))]
                
            if pos < len(line):
                saw_char = True
                if getsize:
                    last_glyph_height = getimgheight(glyph_dict[glyphs[-1][1]])
                            
            # Make sure there's at least something to preserve the vertical space gap
            if not saw_char:
                if not glyph_dict.has_key((' ', cur_font_name, cur_font_size, cur_color)):
                    glyph_dict[(' ', cur_font_name, cur_font_size, cur_color)] = cur_font.render(' ', antialias, cur_color)
                glyphs.append((' ', (' ', cur_font_name, cur_font_size, cur_color)))
                
            
            lines.append(glyphs)
            
        # Split up lines that are too long, if needed
        if wordwrap:
            lines = Graphics.do_word_wrap(lines, wrapwidth, glyph_dict)
                        
        # Now we've processed all the commands and done the pre-rendering for
        # all the characters we'll be displaying. Go through line by line and
        # produce images for each one.
        dy = 0  # The default y offset
        line_surfaces = []
        line_spacing = 1
        total_height = 0
        max_width = 0
        alignment = 'l'
        for line in lines:
            x = 0
            dytmp = dy
            # First, we need to find the bounding rectangle for this line
            bounding_rect = pygame.Rect(0,0,0,0)
            for c,glyph in line:
                if c == None:
                    if glyph.has_key('dx'):
                        x += glyph['dx']
                    if glyph.has_key('dy'):
                        dy = glyph['dy']
                    if glyph.has_key('line_spacing'):
                        line_spacing = glyph['line_spacing']
                    if glyph.has_key('alignment'):
                        alignment = glyph['alignment']
                else:
                    # Add in the current glyph's rectangle
                    glyph_rect = glyph_dict[glyph].get_rect()
                    bounding_rect.union_ip(glyph_rect.move(x,dy))
                    x += glyph_rect.width
            
            # Add the line to the list of surfaces, saving the height / width
            max_width = max(max_width, bounding_rect.width)
            height = line_spacing * bounding_rect.height
            total_height += height
            line_surfaces.append((line, bounding_rect, height, alignment))

        if wordwrap:
            max_width = max(max_width, wrapwidth)
            
        if getsize:
            return max_width, total_height
        # Create the final image and blit all the lines to it
        text_image = pygame.Surface((max_width, total_height)).convert_alpha()
        text_image.fill(backgroundcolor)
        y = 0
        w = text_image.get_rect().width
        for surface,bounding_rect, height,alignment in line_surfaces:
            x = 0
            #print alignment
            if alignment == 'r':
                x = w - bounding_rect.width
            elif alignment == 'c':
                x = w/2 - bounding_rect.width / 2
            
            # We know the bounding rectangle, create the surface on which to render the line
            #line_surface = pygame.Surface((bounding_rect.width, height)).convert_alpha()
            #line_surface.fill(backgroundcolor)
            #x = 0
            dy = y
            for c,glyph in surface:
                if c == None:
                    if glyph.has_key('dx'):
                        x += glyph['dx']
                    if glyph.has_key('dy'):
                        dy = glyph['dy']
                    if glyph.has_key('spacing'):
                        line_spacing = glyph['spacing']
                    if glyph.has_key('alignment'):
                        alignment = glyph['alignment']
                else:
                    # This is a glyph -- draw it
                    text_image.blit(glyph_dict[glyph], (x - bounding_rect.left, dy - bounding_rect.top))
                    x += getimgwidth(glyph_dict[glyph])

            y += height
                
        t2 = time.time()
        #print "RENDERING TOOK %f with method %d" % (t2-t1, Graphics.TEXT_RENDER_METHOD)
        return text_image