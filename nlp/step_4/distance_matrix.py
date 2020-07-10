import pandas as pd
from recipe_recommendation.Recomend.recommend_main import *

if __name__ == '__main__':
    source_path = '../../../data/nlp_data/source_embedding.csv'
    recipe_path = '../../../data/nlp_data/recipe_embedding.csv'
    sourceFrame = pd.read_csv(source_path, index_col=3)
    recipeFrame = pd.read_csv(recipe_path)

    print(sourceFrame.shape,'\n',sourceFrame)

    all_sources = sourceFrame.index

    sources_point_dict = { source:(sourceFrame.loc[source, 'x'],
                                  sourceFrame.loc[source, 'y'],
                                  sourceFrame.loc[source, 'z']) for source in all_sources }

    all_recipe_info = []

    for idx,recipe in recipeFrame.iterrows():
        print(recipe.title)
        recipe_row_dict = dict()
        recipe_row_dict['id'] = recipe.id
        recipe_row_dict['cat1'] = recipe.cat1
        recipe_row_dict['cat2'] = recipe.cat2
        recipe_row_dict['cat3'] = recipe.cat3
        recipe_row_dict['cat4'] = recipe.cat4
        recipe_row_dict['title'] = recipe.title

        recipe_row_dict.update({source:None for source in all_sources})

        recipe_point = (recipe.x, recipe.y, recipe.z)
        recipe_sources = recipe.kwd_source.split('|')

        # 있는 식재료의 거리만 구할것이다.
        for source in recipe_sources:
            try:
                recipe_row_dict[source] = calculate_distance(sources_point_dict[source],
                                                             recipe_point)
            except KeyError as err:
                pass
        all_recipe_info.append(recipe_row_dict)

    FlaskFrame = pd.DataFrame(all_recipe_info)
    print(FlaskFrame.shape)

    flask_path = '../../../data/nlp_data/recommend_data.csv'
    FlaskFrame.to_csv(flask_path,index=False)

    # flask_path = '../../../data/nlp_data/recommend_data.csv'
    # FlaskFrame = pd.read_csv(flask_path,index_col=(1,2,3,4))
    #
    # start = time.time()
    #
    # cat1 = slice(None)
    # cat2 = slice(None)
    # cat3 = slice(None)
    # cat4 = slice(None)
    # m = [slice(None),('일상'),slice(None),('밑반찬')]
    # print(FlaskFrame.loc[m,('id','title','고기','고추')])
    # frame_None = FlaskFrame.loc[(slice(None), ('일상'), slice(None), ('밑반찬')), ('id','title','고기', '고추')]
    # frame_None = frame_None.dropna()
    # print(list(frame_None.columns))
    # print(frame_None.sort_values(by=list(frame_None.columns)[2:]))
    #
    # final_recipe_dict = dict()
    #
    # for source in list(frame_None.columns)[2:]:
    #     source_frame = frame_None.loc[:,('id','title',source)].sort_values(by=(source))[0:5]
    #     final_recipe_dict.update({ d[0]:d[1] for d in zip(source_frame.id,source_frame.title)})
    #
    # print(final_recipe_dict)
    #
    # print(time.time() - start)