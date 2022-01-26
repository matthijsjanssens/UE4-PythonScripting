import unreal

assets = unreal.EditorAssetLibrary.list_assets('/Game/')

print(f'{len(assets)} assets found')

for asset in assets[:10]:
    print(asset)

unreal.EditorAssetLibrary.find_asset_data('/Game/SM_Test.SM_Test').get_asset().static_class()