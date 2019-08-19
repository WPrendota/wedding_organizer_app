import base64
from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import WeddingForm, TableForm, GuestForm

from .models import Wedding, Table, Guest
from PIL import Image, ImageFont, ImageDraw


@login_required
def wedding_organizer_app(request):
    content = {
    }
    return render(request, 'wedding_organizer_app/wedding_organizer_app.html', content)


@login_required
def new_wedding(request):
    if request.method == 'POST':
        form_w = WeddingForm(request.POST)

        if form_w.is_valid():
            weddings = Wedding.objects.filter(user=request.user)

            if not weddings:
                form_w = form_w.save(commit=False)
                form_w.user = request.user
                form_w.save()
                messages.success(request, "Added new wedding!")
                return redirect('wedding_organizer_app_management')

            for wedding in weddings:
                if form_w.cleaned_data['hall_name'] == wedding.hall_name and wedding.user == request.user:
                    messages.warning(request, "Wedding name taken!")
                    print("Wedding name taken!")
                    return redirect('new_wedding')

            form_w = form_w.save(commit=False)
            form_w.user = request.user
            form_w.save()
            messages.success(request, "Added new wedding!")
            return redirect('wedding_organizer_app_management')
    else:
        form_w = WeddingForm()

    content = {'form_w': form_w,
               }
    return render(request, 'wedding_organizer_app/new_wedding.html', content)


@login_required
def wedding_organizer_app_management(request):

    content = {
               }
    return render(request, 'wedding_organizer_app/wedding_management.html', content)


@login_required
def add_guest(request):
    if request.method == 'POST':
        form_g = GuestForm(request.user, request.POST)

        if form_g.is_valid():
            guests = Guest.objects.filter(user=request.user)

            if not guests:
                form_g = form_g.save(commit=False)
                form_g.user = request.user
                form_g.save()
                messages.success(request, "Added new guest!")
                return redirect('wedding_organizer_app_management')
            else:
                for guest in guests:
                    print(form_g.cleaned_data['chair_number'])
                    print(guest.chair_number)
                    if form_g.cleaned_data['chair_number'] == guest.chair_number:
                        print("Chair number taken!")
                        messages.warning(request, "Chair number taken! Please change.")
                        return redirect('add_guest')
                    elif int(form_g.cleaned_data['chair_number']) >= guest.table.max_size:
                        print("Table maximum size: " + str(guest.table.max_size))
                        messages.warning(request, "Table maximum size is: " + str(guest.table.max_size) + "! Please change.")
                        return redirect('add_guest')

                form_g = form_g.save(commit=False)
                form_g.user = request.user
                form_g.save()
                messages.success(request, "Added new guest!")
                return redirect('wedding_organizer_app_management')
    else:
        form_g = GuestForm(request.user)

    content = {'form_g': form_g,
               }
    return render(request, 'wedding_organizer_app/add_guest.html', content)


@login_required
def add_table(request):
    if request.method == 'POST':
        form_t = TableForm(request.user, request.POST)

        if form_t.is_valid():
            tables = Table.objects.filter(user=request.user)

            if not tables:
                form_t = form_t.save(commit=False)
                form_t.user = request.user
                form_t.save()
                messages.success(request, "Added new table!")
                return redirect('wedding_organizer_app_management')

            for table in tables:
                if form_t.cleaned_data['number'] == table.number and table.user == request.user:
                    messages.warning(request, "Table number taken!")
                    print("Table number taken!")
                    return redirect('add_table')

            form = form_t.save(commit=False)
            form.user = request.user
            form.wedding = form_t.cleaned_data['wedding']
            form.save()
            messages.success(request, "Added new table!")
            return redirect('wedding_organizer_app_management')
    else:
        form_t = TableForm(request.user)

    content = {'form_t': form_t,
               }
    return render(request, 'wedding_organizer_app/add_table.html', content)


def tables_guest_filter(table, guests):
    guests_filtered = []

    for guest in guests:
        if guest.table == table:
            guests_filtered.append(guest)

    return guests_filtered


# The method for drawing a wedding hall in .html page:
@login_required
def generate_halls(request):
    weddings = Wedding.objects.filter(user=request.user)
    tables = Table.objects.filter(user=request.user)
    guests = Guest.objects.filter(user=request.user)

    table_spots_images = []

    for table in tables:
        table_spots_images.append(createHallImage(table, tables_guest_filter(table, guests)))

    content = {'weddings': weddings,
               'tables': tables,
               'guests': guests,
                'table_spots_images': table_spots_images,
               }
    return render(request, 'wedding_organizer_app/generate_halls.html', content)


# Draw table with assigned guests
def createHallImage(table, guests):
    # Initial Chair size:
    chair_height = 100
    chair_width = 50

    # Add Text Font Type:
    chair_font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSerif.ttf", 10, encoding="unic")
    table_font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSerif.ttf", 20, encoding="unic")

    # Draw table and chairs area:
    table_spot_image = Image.new('RGBA', (int(table.max_size/2) * chair_width + int(table.max_size/2) * 15,
                                          2 * chair_height + int(chair_height/2)), "grey")

    # Draw table:
    table_image = Image.new('RGBA', (int(table.max_size/2) * chair_width + int(table.max_size/2) * 15,
                                     int(chair_height/2)), color=(222, 184, 135))

    # Add Table Data Informations:
    text_draw = ImageDraw.Draw(table_image)
    text_draw.text((int(table_image.width/2)-int(table_image.height/3),
                    int(table_image.height/2)-int(table_image.height/5)),
                   "Table: " + str(table.number),
                   font=table_font, fill=(0, 0, 0))

    # Draw and add chairs to the right spots:
    for loop_counter in range(table.max_size):
        for guest_number, guest in enumerate(guests):
            if loop_counter < (table.max_size/2) and loop_counter == guest.chair_number:
                # Chair image creation:
                chair_image = Image.new('RGBA', (chair_height, chair_width), color=(139,69,19))

                # Add Guests Data Informations:
                text_draw = ImageDraw.Draw(chair_image)
                text_draw.text((1,0),  guest.title + "\n" + guest.first_name + "\n" + guest.second_name
                               + "\n" + guest.family_side, font=chair_font,  fill=(250, 250, 250))

                # Image Rotation:
                chair_image = chair_image.rotate(90, expand=1)

                # Images Connection
                table_spot_image.paste(chair_image,
                                       (10+(guest.chair_number*(10 + chair_width)),
                                        0))
            elif (table.max_size/2) <= loop_counter < table.max_size and loop_counter == guest.chair_number:
                # Chair image creation:
                chair_image = Image.new('RGBA', (chair_height, chair_width), color=(139,69,19))

                # Add Guests Data Informations:
                text_draw = ImageDraw.Draw(chair_image)
                text_draw.text((1, 0), guest.title + "\n" + guest.first_name + "\n" + guest.second_name
                               + "\n" + guest.family_side, font=chair_font, fill=(250, 250, 250))

                # Image Rotation:
                chair_image = chair_image.rotate(90, expand=1)

                # Images Connection
                table_spot_image.paste(chair_image,
                                       (10 + ((guest.chair_number-int(table.max_size/2)) * (10 + chair_width)),
                                        chair_height+int(chair_height/2)))

    # Add table to spot:
    table_spot_image.paste(table_image, (0, chair_height))

    buf = BytesIO()
    table_spot_image.save(buf, format="GIF")
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()
    return image_base64
