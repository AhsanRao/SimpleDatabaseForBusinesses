from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user
)
from flask_dance.contrib.github import github
from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.models import Users
from apps.authentication.util import verify_pass
from apps.authentication.models import AuctionItem
from flask_login import login_required
import pandas as pd
from io import BytesIO
from flask import Response
from flask import flash
from sqlalchemy.exc import IntegrityError
from flask import jsonify
from sqlalchemy import or_
from sqlalchemy.orm import aliased

from .models import db, Person, Address, PhoneNumber, Equipment, Contract, ContractEquipment

@blueprint.route('/add-record', methods=['GET', 'POST'])
@login_required
def add_record():
    if request.method == 'POST':
        try:
            # Get data from form
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            gender = request.form['gender']
            email = request.form['email']
            role = request.form['role']

            street = request.form['street']
            city = request.form['city']
            state = request.form['state']
            zipcode = request.form['zipcode']
            country = request.form['country']

            home_phone = request.form['home_phone']
            business_phone = request.form['business_phone']

            # Create new instances of the models
            new_person = Person(first_name=first_name, last_name=last_name, gender=gender, email=email, role=role)

            new_address = Address(street=street, city=city, state=state, zipcode=zipcode, country=country, person_id=new_person.person_id)
            new_phone_number = PhoneNumber(home_phone_number=home_phone, business_phone_number=business_phone, person_id=new_person.person_id)

            db.session.add(new_person)
            db.session.flush()  # Flush the changes to assign an ID to new_person
            # Add new records to the database
            db.session.add(new_address)
            db.session.add(new_phone_number)
            db.session.commit()

            flash('Record added successfully!', 'success')
            return redirect(url_for('authentication_blueprint.add_record'))

        except IntegrityError as e:
            db.session.rollback()
            form_data = request.form  # Capture the form data
            if "Duplicate entry" in str(e):
                flash("Email already in use. Please use a different email.", "error")
            else:
                flash("A database error occurred. Please try again.", "error")
            return render_template('home/addrecord.html', form_data=form_data)

        except Exception as e:
            db.session.rollback()
            form_data = request.form
            flash("An unexpected error occurred: " + str(e), "error")
            return render_template('home/addrecord.html', form_data=form_data)

    return render_template('home/addrecord.html', form_data={}, segment='record')


@blueprint.route('/add-user', methods=['GET', 'POST'])
@login_required
def add_user():
    if request.method == 'POST':
        try:
            # Get data from form
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            gender = request.form['gender']
            email = request.form['email']
            role = request.form['role']

            street = request.form['street']
            city = request.form['city']
            state = request.form['state']
            zipcode = request.form['zipcode']
            country = request.form['country']

            home_phone = request.form['home_phone']
            business_phone = request.form['business_phone']

            # Create new instances of the models
            new_person = Person(first_name=first_name, last_name=last_name, gender=gender, email=email, role=role)

            db.session.add(new_person)
            db.session.flush()  # Flush the changes to assign an ID to new_person

            new_address = Address(street=street, city=city, state=state, zipcode=zipcode, country=country, person_id=new_person.person_id)
            new_phone_number = PhoneNumber(home_phone_number=home_phone, business_phone_number=business_phone, person_id=new_person.person_id)

            # Add new users to the database
            db.session.add(new_address)
            db.session.add(new_phone_number)
            db.session.commit()

            flash('User added successfully!', 'success')
            return redirect(url_for('authentication_blueprint.add_user'))

        except IntegrityError as e:
            db.session.rollback()
            form_data = request.form  # Capture the form data
            if "Duplicate entry" in str(e):
                flash("Email already in use. Please use a different email.", "error")
            else:
                flash("A database error occurred. Please try again.", "error")
            return render_template('home/adduser.html', form_data=form_data)

        except Exception as e:
            db.session.rollback()
            form_data = request.form
            flash("An unexpected error occurred: " + str(e), "error")
            return render_template('home/adduser.html', form_data=form_data)

    return render_template('home/adduser.html', form_data={}, segment='user')

@blueprint.route('/add-equipment', methods=['GET', 'POST'])
@login_required
def add_equipment():
    if request.method == 'POST':
        try:
            # Get data from form
            asset_tag_number = request.form['asset_tag_number']
            equipment_name = request.form['equipment_name']
            serial_number = request.form['serial_number']
            install_date = request.form['install_date']

            # Create new instance of the Equipment model
            new_equipment = Equipment(asset_tag_number=asset_tag_number, equipment_name=equipment_name, serial_number=serial_number, install_date=install_date)

            db.session.add(new_equipment)
            db.session.commit()

            flash('Equipment added successfully!', 'success')
            return redirect(url_for('authentication_blueprint.add_equipment'))

        except IntegrityError as e:
            db.session.rollback()
            form_data = request.form  # Capture the form data
            if "Duplicate entry" in str(e):
                flash("Asset Tag Number already in use. Please use a different number.", "error")
            else:
                flash("A database error occurred. Please try again.", "error")
            return render_template('home/addequipment.html', form_data=form_data)

        except Exception as e:
            db.session.rollback()
            form_data = request.form
            flash("An unexpected error occurred: " + str(e), "error")
            return render_template('home/addequipment.html', form_data=form_data)

    return render_template('home/addequipment.html', form_data={}, segment='equipment')

@blueprint.route('/find-user')
def find_user():
    email = request.args.get('email')
    user = Person.query.filter_by(email=email).first()
    if user:
        address = Address.query.filter_by(person_id=user.person_id).first()
        if address:
            address_info = f"{address.street}, {address.city}, {address.state}, {address.country}"
            zipcode = f"{address.zipcode}"
        else:
            address_info = "No address on file"
        phone = PhoneNumber.query.filter_by(person_id=user.person_id).first()
        if phone:
            home_phone = f"{phone.home_phone_number}"
            business_phone = f"{phone.business_phone_number}"
        else:
            home_phone = "No phone number on file"
            business_phone = "No phone number on file"
        if user.gender == 'M':
            gender = "Male"
        elif user.gender == 'F':
            gender = "Female"

        return jsonify({
            'success': True,
            'full_name': user.first_name + ' ' + user.last_name,
            'zipcode': zipcode,
            'role': user.role,
            'address': address_info,
            'home_phone': home_phone,
            'gender': gender,
            'business_phone': business_phone
        })
    return jsonify({'success': False, 'message': 'User not found'})

def get_user_info(user):
    address = Address.query.filter_by(person_id=user.person_id).first()
    if address:
        address_info = f"{address.street}, {address.city}, {address.state}, {address.country}"
        zipcode = f"{address.zipcode}"
    else:
        address_info = "No address on file"

    phone = PhoneNumber.query.filter_by(person_id=user.person_id).first()
    if phone:
        home_phone = f"{phone.home_phone_number}"
        business_phone = f"{phone.business_phone_number}"
    else:
        home_phone = "No phone number on file"
        business_phone = "No phone number on file"

    if user.gender == 'M':
        gender = "Male"
    elif user.gender == 'F':
        gender = "Female"
    else:
        gender = "Other or not specified"

    return {
        'full_name': user.first_name + ' ' + user.last_name,
        'zipcode': zipcode,
        'role': user.role,
        'address': address_info,
        'home_phone': home_phone,
        'gender': gender,
        'business_phone': business_phone
    }

@blueprint.route('/find-client')
def find_client():
    email = request.args.get('email')
    user = Person.query.filter_by(email=email, role="Client").first()
    if user:
        address = Address.query.filter_by(person_id=user.person_id).first()
        phone = PhoneNumber.query.filter_by(person_id=user.person_id).first()

        address_info = f"{address.street}, {address.city}, {address.state}, {address.country}" if address else "No address on file"
        zipcode = f"{address.zipcode}" if address else "No zipcode on file"
        home_phone = f"{phone.home_phone_number}" if phone else "No phone number on file"
        business_phone = f"{phone.business_phone_number}" if phone else "No phone number on file"
        gender = "Male" if user.gender == 'M' else "Female" if user.gender == 'F' else "Other or not specified"

        return jsonify({
            'success': True,
            'full_name': user.first_name + ' ' + user.last_name,
            'zipcode': zipcode,
            'role': user.role,
            'address': address_info,
            'home_phone': home_phone,
            'gender': gender,
            'business_phone': business_phone
        })
    return jsonify({'success': False, 'message': 'Client not found'})


@blueprint.route('/find-sales')
def find_sales():
    email = request.args.get('email')
    user = Person.query.filter(Person.email == email, Person.role != "Client").first()
    if user:
        address = Address.query.filter_by(person_id=user.person_id).first()
        phone = PhoneNumber.query.filter_by(person_id=user.person_id).first()

        address_info = f"{address.street}, {address.city}, {address.state}, {address.country}" if address else "No address on file"
        zipcode = f"{address.zipcode}" if address else "No zipcode on file"
        home_phone = f"{phone.home_phone_number}" if phone else "No phone number on file"
        business_phone = f"{phone.business_phone_number}" if phone else "No phone number on file"
        gender = "Male" if user.gender == 'M' else "Female" if user.gender == 'F' else "Other or not specified"

        return jsonify({
            'success': True,
            'full_name': user.first_name + ' ' + user.last_name,
            'zipcode': zipcode,
            'role': user.role,
            'address': address_info,
            'home_phone': home_phone,
            'gender': gender,
            'business_phone': business_phone
        })
    return jsonify({'success': False, 'message': 'SalesExecutive not found'})


@blueprint.route('/find-equipment')
def find_equipment():
    asset_tag_number = request.args.get('asset_tag_number')
    equipment = Equipment.query.filter_by(asset_tag_number=asset_tag_number).first()
    if equipment:
        return jsonify({
            'success': True,
            'equipment_name': equipment.equipment_name,
            'serial_number': equipment.serial_number,
            'install_date': equipment.install_date.isoformat() if equipment.install_date else ''
        })
    return jsonify({'success': False, 'message': 'Equipment not found'})


@blueprint.route('/add-contract', methods=['GET', 'POST'])
@login_required
def add_contract():
    if request.method == 'POST':
        try:
            # Extract contract data from form
            contract_id = request.form.get('contract_id')
            installation_date = request.form.get('installation_date')
            monthly_charges = request.form.get('monthly_charges')
            billing_date = request.form.get('billing_date')
            renewal_date = request.form.get('renewal_date')

            # Fetch client details
            email = request.form['email']
            client = Person.query.filter_by(email=email).first()

            print(client.first_name, client.last_name)
            if not client:
                flash('Client not found.', 'error')
                return redirect(url_for('authentication_blueprint.add_contract'))

            # Fetch salesperson details
            semail = request.form['sale-email']  # Salesperson email

            salesperson = Person.query.filter_by(email=semail).first()

            if not salesperson:
                flash('Salesperson not found.', 'error')
                return redirect(url_for('authentication_blueprint.add_contract'))

            # Fetch equipment details
            tag = request.form['asset_tag_number']

            equipment = Equipment.query.filter_by(asset_tag_number=tag).first()

            if not equipment:
                flash('Equipment not found.', 'error')
                return redirect(url_for('authentication_blueprint.add_contract'))

            # Create and add a new contract
            new_contract = Contract(installation_date=installation_date, monthly_charges=monthly_charges, 
                                    billing_date=billing_date, renewal_date=renewal_date, 
                                    person_id=salesperson.person_id, role=salesperson.role)
            db.session.add(new_contract)

            db.session.flush()  # Flush to get the contract ID

            # Create and add a new entry in contract_equipments table
            new_contract_equipment = ContractEquipment(contract_id=new_contract.contract_id, 
                                                       equipment_id=equipment.equipment_id, 
                                                       person_id=client.person_id)
            db.session.add(new_contract_equipment)

            # Commit the changes
            db.session.commit()
            flash('Contract created successfully!', 'success')

        except IntegrityError as e:
            db.session.rollback()
            form_data = request.form
            flash('A database error occurred. Please try again.', 'error')

        except Exception as e:
            db.session.rollback()
            form_data = request.form
            flash('An unexpected error occurred: ' + str(e), 'error')

        return render_template('home/addcontract.html', form_data={}, segment='contract')

    return render_template('home/addcontract.html', form_data={}, segment='contract')


@blueprint.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    # Fetch unique values for filters
    businesses = db.session.query(AuctionItem.business).distinct().all()
    bids = ["with", "without"]  # Manually defined
    reserves = [reserve[0] for reserve in db.session.query(AuctionItem.reserve).distinct().all()]
    auction_statuses = [status[0] for status in db.session.query(AuctionItem.status).distinct().all()]
    
    # Extract sort criteria from the request
    sort_column = request.args.get('sort_column', default='id')  # default to 'id' column if not provided
    sort_direction = request.args.get('sort_direction', default='asc')  # default to ascending if not provided
    
    # Extract search term from the request
    search_term = request.form.get('search_term', '').strip()
    
    if request.method == 'POST':
        # Get filter criteria from form
        business_filter = request.form.get('Business')
        reserve_filter = request.form.get('reserve')
        bids_filter = request.form.get('bids')
        status_filter = request.form.get('auctionStatus')
        
        # Create a query based on filter criteria
        query = AuctionItem.query
        if business_filter:
            query = query.filter(AuctionItem.business == business_filter)
        if reserve_filter:
            query = query.filter(AuctionItem.reserve == reserve_filter)
        if bids_filter:
            if bids_filter == 'with':
                query = query.filter(AuctionItem.bids > 0)
            else:
                query = query.filter(AuctionItem.bids == 0)
                
        if status_filter:
            query = query.filter(AuctionItem.status == status_filter)
            
        # Add sorting to the query
        if sort_direction == 'asc':
            query = query.order_by(getattr(AuctionItem, sort_column).asc())
        else:
            query = query.order_by(getattr(AuctionItem, sort_column).desc())
            
        # Add search term to the query
        # if search_term:
        #     query = query.filter(AuctionItem.title.ilike(f"%{search_term}%"))
        # For every field search term
        if search_term:
            search_filter = or_(
                AuctionItem.title.ilike(f"%{search_term}%"),
                AuctionItem.description.ilike(f"%{search_term}%"),
                AuctionItem.business.ilike(f"%{search_term}%"),
                AuctionItem.status.ilike(f"%{search_term}%"),
                # Add other fields as needed
            )
            query = query.filter(search_filter)
                
        # Execute the query
        auction_items = query.limit(500).all()
    else:
        # Default behavior when the page is loaded
        # if search_term:
        #     auction_items = AuctionItem.query.filter(AuctionItem.title.ilike(f"%{search_term}%")).order_by(getattr(AuctionItem, sort_column).send(sort_direction)()).limit(100).all()
        # for every field
        if search_term:
            search_filter = or_(
                AuctionItem.title.ilike(f"%{search_term}%"),
                AuctionItem.description.ilike(f"%{search_term}%"),
                AuctionItem.business.ilike(f"%{search_term}%"),
                AuctionItem.status.ilike(f"%{search_term}%"),
            )
            auction_items = AuctionItem.query.filter(search_filter).order_by(getattr(AuctionItem, sort_column).send(sort_direction)()).limit(100).all()

        # auction_items = AuctionItem.query.limit(100).all()
        sorting_method = getattr(getattr(AuctionItem, sort_column), sort_direction)
        auction_items = AuctionItem.query.order_by(sorting_method()).limit(500).all()

    # return render_template('home/auction_items.html', auction_items=auction_items, segment='filterauction')
    return render_template(
        'home/auction_items.html', 
        auction_items=auction_items,
        businesses=businesses,
        reserves=reserves,
        bids=bids,
        auction_statuses=auction_statuses,
        segment='search'
    )

@blueprint.route('/search-user', methods=['GET', 'POST'])
@login_required
def search_user():
    # Extract search term from the request
    search_term = request.form.get('search_term', '').strip()

    if request.method == 'POST':
        if search_term:
            search_filter = or_(
                Person.person_id.ilike(f"%{search_term}%"),
                Person.first_name.ilike(f"%{search_term}%"),
                Person.last_name.ilike(f"%{search_term}%"),
                Person.email.ilike(f"%{search_term}%"),
                Person.role.ilike(f"%{search_term}%"),
                Person.gender.ilike(f"%{search_term}%"),
                Address.street.ilike(f"%{search_term}%"),
                Address.city.ilike(f"%{search_term}%"),
                Address.state.ilike(f"%{search_term}%"),
                Address.zipcode.ilike(f"%{search_term}%"),
                Address.country.ilike(f"%{search_term}%"),
                PhoneNumber.home_phone_number.ilike(f"%{search_term}%"),
                PhoneNumber.business_phone_number.ilike(f"%{search_term}%")
            )
            users = db.session.query(Person, Address, PhoneNumber)\
                .join(Address, Address.person_id == Person.person_id)\
                .join(PhoneNumber, PhoneNumber.person_id == Person.person_id)\
                .filter(search_filter)\
                .all()
        else:
            users = db.session.query(Person, Address, PhoneNumber)\
                .join(Address, Address.person_id == Person.person_id)\
                .join(PhoneNumber, PhoneNumber.person_id == Person.person_id)\
                .all()
    else:
        users = db.session.query(Person, Address, PhoneNumber)\
            .join(Address, Address.person_id == Person.person_id)\
            .join(PhoneNumber, PhoneNumber.person_id == Person.person_id)\
            .all()

    return render_template(
        'home/searchuser.html',
        users=users,
        segment='search-us'
    )


@blueprint.route('/search-equipment', methods=['GET', 'POST'])
@login_required
def search_equipment():
    # Extract search term from the request
    search_term = request.form.get('search_term', '').strip()

    if request.method == 'POST':
        # Create a query based on the search term
        if search_term:
            search_filter = or_(
                Equipment.equipment_id.ilike(f"%{search_term}%"),
                Equipment.asset_tag_number.ilike(f"%{search_term}%"),
                Equipment.equipment_name.ilike(f"%{search_term}%"),
                Equipment.serial_number.ilike(f"%{search_term}%"),
                Equipment.install_date.ilike(f"%{search_term}%")
            )
            equipments = Equipment.query.filter(search_filter).all()
        else:
            # If no search term, display all users 
            equipments = Equipment.query.all()
    else:
        # Default behavior when the page is loaded
        equipments = Equipment.query.all()

    return render_template(
        'home/searchequipment.html',
        equipments=equipments,
        segment='search-eq'
    )


@blueprint.route('/search-contract', methods=['GET', 'POST'])
@login_required
def search_contract():
    search_term = request.form.get('search_term', '').strip()

    # Aliases for the client and sales executive
    Client = aliased(Person)
    SalesExecutive = aliased(Person)
    ClientAddress = aliased(Address)
    ClientPhoneNumber = aliased(PhoneNumber)
    SalesExecutiveAddress = aliased(Address)
    SalesExecutivePhoneNumber = aliased(PhoneNumber)

    if request.method == 'POST' and search_term:
        # Define search filter
        search_filter = or_(
            # Client Details
            Client.first_name.ilike(f"%{search_term}%"),
            Client.last_name.ilike(f"%{search_term}%"),
            Client.email.ilike(f"%{search_term}%"),
            Client.role.ilike(f"%{search_term}%"),
            Client.gender.ilike(f"%{search_term}%"),

            # Sales Executive Details
            SalesExecutive.first_name.ilike(f"%{search_term}%"),
            SalesExecutive.last_name.ilike(f"%{search_term}%"),
            SalesExecutive.email.ilike(f"%{search_term}%"),
            SalesExecutive.role.ilike(f"%{search_term}%"),

            # Address Details (both Client and Sales Executive)
            ClientAddress.street.ilike(f"%{search_term}%"),
            ClientAddress.city.ilike(f"%{search_term}%"),
            ClientAddress.state.ilike(f"%{search_term}%"),
            ClientAddress.zipcode.ilike(f"%{search_term}%"),
            ClientAddress.country.ilike(f"%{search_term}%"),
            SalesExecutiveAddress.street.ilike(f"%{search_term}%"),
            SalesExecutiveAddress.city.ilike(f"%{search_term}%"),
            SalesExecutiveAddress.state.ilike(f"%{search_term}%"),
            SalesExecutiveAddress.zipcode.ilike(f"%{search_term}%"),
            SalesExecutiveAddress.country.ilike(f"%{search_term}%"),

            # Phone Number Details (both Client and Sales Executive)
            ClientPhoneNumber.home_phone_number.ilike(f"%{search_term}%"),
            ClientPhoneNumber.business_phone_number.ilike(f"%{search_term}%"),
            SalesExecutivePhoneNumber.home_phone_number.ilike(f"%{search_term}%"),
            SalesExecutivePhoneNumber.business_phone_number.ilike(f"%{search_term}%"),

            # Equipment Details
            Equipment.asset_tag_number.ilike(f"%{search_term}%"),
            Equipment.equipment_name.ilike(f"%{search_term}%"),
            Equipment.serial_number.ilike(f"%{search_term}%"),

            # Contract Details
            Contract.contract_id.ilike(f"%{search_term}%"),
            Contract.installation_date.ilike(f"%{search_term}%"),
            Contract.billing_date.ilike(f"%{search_term}%"),
            Contract.renewal_date.ilike(f"%{search_term}%"),
            Contract.monthly_charges.ilike(f"%{search_term}%")
        )

        contracts = db.session.query(Contract, Client, Equipment, ClientAddress, ClientPhoneNumber, SalesExecutive, SalesExecutiveAddress, SalesExecutivePhoneNumber)\
            .join(ContractEquipment, Contract.contract_id == ContractEquipment.contract_id)\
            .join(Client, ContractEquipment.person_id == Client.person_id)\
            .join(SalesExecutive, Contract.person_id == SalesExecutive.person_id)\
            .join(Equipment, ContractEquipment.equipment_id == Equipment.equipment_id)\
            .outerjoin(ClientAddress, Client.person_id == ClientAddress.person_id)\
            .outerjoin(ClientPhoneNumber, Client.person_id == ClientPhoneNumber.person_id)\
            .outerjoin(SalesExecutiveAddress, SalesExecutive.person_id == SalesExecutiveAddress.person_id)\
            .outerjoin(SalesExecutivePhoneNumber, SalesExecutive.person_id == SalesExecutivePhoneNumber.person_id)\
            .filter(search_filter)\
            .all()
    else:
        contracts = db.session.query(Contract, Client, Equipment, ClientAddress, ClientPhoneNumber, SalesExecutive, SalesExecutiveAddress, SalesExecutivePhoneNumber)\
            .join(ContractEquipment, Contract.contract_id == ContractEquipment.contract_id)\
            .join(Client, ContractEquipment.person_id == Client.person_id)\
            .join(SalesExecutive, Contract.person_id == SalesExecutive.person_id)\
            .join(Equipment, ContractEquipment.equipment_id == Equipment.equipment_id)\
            .outerjoin(ClientAddress, Client.person_id == ClientAddress.person_id)\
            .outerjoin(ClientPhoneNumber, Client.person_id == ClientPhoneNumber.person_id)\
            .outerjoin(SalesExecutiveAddress, SalesExecutive.person_id == SalesExecutiveAddress.person_id)\
            .outerjoin(SalesExecutivePhoneNumber, SalesExecutive.person_id == SalesExecutivePhoneNumber.person_id)\
            .all()

    return render_template(
        'home/searchcontract.html',
        contracts=contracts,
        segment='search-con'
    )



@blueprint.route('/exportauction', methods=['POST'])
@login_required
def exportauction():
    # Get filter criteria from form
    business_filter = request.form.get('Business')
    reserve_filter = request.form.get('reserve')
    bids_filter = request.form.get('bids')
    status_filter = request.form.get('auctionStatus')
    
    # Create a query based on filter criteria
    query = AuctionItem.query
    if business_filter:
        query = query.filter(AuctionItem.business == business_filter)
    if reserve_filter:
        query = query.filter(AuctionItem.reserve == reserve_filter)
    if bids_filter:
        if bids_filter == 'with':
            query = query.filter(AuctionItem.bids > 0)
        else:
            query = query.filter(AuctionItem.bids == 0)
    if status_filter:
        query = query.filter(AuctionItem.status == status_filter)
    
    # Execute the query
    auction_items = query.all()

    records = [item.to_dict() for item in auction_items]

    # Return the data as an Excel file
    if not records:
        return "No data to export", 400
    df = pd.DataFrame(records)
    output = BytesIO()  # Create an in-memory bytes buffer
    df.to_excel(output, index=False, engine='openpyxl')  # Write the DataFrame to the buffer
    output.seek(0)  # Go back to the start of the buffer

    response = Response(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response.headers["Content-Disposition"] = "attachment; filename=auction_data.xlsx"
    
    return response

@blueprint.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    # Get data from form
    first_name = request.form.get('fn')
    last_name = request.form.get('ln')
    address = request.form.get('add')
    about_info = request.form.get('abt')

    # Update user in the database
    user = Users.query.get(current_user.id)
    if user:
        user.first_name = first_name
        user.last_name = last_name
        user.address = address
        user.about_info = about_info
        db.session.commit()

    return redirect(url_for('profile_page_route')) # Redirect to the profile page after updating

@blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        # Handle profile updates here
        current_user.first_name = request.form.get('fn')
        current_user.last_name = request.form.get('ln')
        current_user.address = request.form.get('add')
        current_user.about = request.form.get('abt')
        db.session.commit()
        # Add a flash message or some notification that the profile was updated
        return redirect(url_for('authentication_blueprint.profile'))

    return render_template('home/profile.html', current_user=current_user)

@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))

# Login & Registration

@blueprint.route("/github")
def login_github():
    """ Github login """
    if not github.authorized:
        return redirect(url_for("github.login"))

    res = github.get("/user")
    return redirect(url_for('home_blueprint.index'))

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        user_id  = request.form['username'] # we can have here username OR email
        password = request.form['password']

        # Locate user
        user = Users.find_by_username(user_id)

        # if user not found
        if not user:

            user = Users.find_by_email(user_id)

            if not user:
                return render_template( 'accounts/login.html',
                                        msg='Unknown User or Email',
                                        form=login_form)

        # Check the password
        if verify_pass(password, user.password):

            login_user(user)
            return redirect(url_for('authentication_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']

        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()

        # Delete user from session
        logout_user()

        return render_template('accounts/register.html',
                               msg='User created successfully.',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login')) 

# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
