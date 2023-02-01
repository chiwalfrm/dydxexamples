#withdrawalamount/maxfee/my_eth_address (SET THESE)
def createfastwithdrawal_creditamount():
        get_fast_withdrawal_result = client.public.get_fast_withdrawal(
                creditAsset = constants.ASSET_USDC,
                creditAmount = withdrawalamount
        )
        lp_position_id_result = list(get_fast_withdrawal_result.data['liquidityProviders'].keys())[0]
        if get_fast_withdrawal_result.data['liquidityProviders'][lp_position_id_result]['quote'] == None:
                print(get_fast_withdrawal_result.data)
                print("ERROR: Could not get a quote")
                sys.exit()
        debit_amount_result = get_fast_withdrawal_result.data['liquidityProviders'][lp_position_id_result]['quote']['debitAmount']
        if float(debit_amount_result) - float(withdrawalamount) > float(maxfee):
                print("ERROR: Fee would exceed maxfee", maxfee)
                sys.exit()
        create_fast_withdrawal_result = client.private.create_fast_withdrawal(
                position_id = account['positionId'],
                credit_asset = constants.ASSET_USDC,
                credit_amount = withdrawalamount,
                debit_amount = debit_amount_result,
                to_address = my_eth_address,
                lp_position_id = lp_position_id_result,
                lp_stark_public_key = list(get_fast_withdrawal_result.data['liquidityProviders'].values())[0]['starkKey'],
                expiration = epoch_seconds_to_iso(time() + 604801)
        )
        print(create_fast_withdrawal_result.data)

#withdrawalamount/maxfee/my_eth_address (SET THESE)
def createfastwithdrawal_debitamount():
        get_fast_withdrawal_result = client.public.get_fast_withdrawal(
                creditAsset = constants.ASSET_USDC,
                debitAmount = withdrawalamount
        )
        lp_position_id_result = list(get_fast_withdrawal_result.data['liquidityProviders'].keys())[0]
        if get_fast_withdrawal_result.data['liquidityProviders'][lp_position_id_result]['quote'] == None:
                print(get_fast_withdrawal_result.data)
                print("ERROR: Could not get a quote")
                sys.exit()
        credit_amount_result = get_fast_withdrawal_result.data['liquidityProviders'][lp_position_id_result]['quote']['creditAmount']
        if float(withdrawalamount) - float(credit_amount_result) > float(maxfee):
                print("ERROR: Fee would exceed maxfee", maxfee)
                sys.exit()
        create_fast_withdrawal_result = client.private.create_fast_withdrawal(
                position_id = account['positionId'],
                credit_asset = constants.ASSET_USDC,
                credit_amount = credit_amount_result,
                debit_amount = withdrawalamount,
                to_address = my_eth_address,
                lp_position_id = lp_position_id_result,
                lp_stark_public_key = list(get_fast_withdrawal_result.data['liquidityProviders'].values())[0]['starkKey'],
                expiration = epoch_seconds_to_iso(time() + 604801)
        )
        print(create_fast_withdrawal_result.data)
