from cluster.kmeans import cluster
import logging


def cluster_checkins(db):
    with db.connection() as c, c.cursor() as curs:
        # Updating entertainments stats. See implementation on the postgres side.
        curs.execute("SELECT update_entertainments_stats();")

        curs.execute("SELECT * FROM entertainments_stats;")
        if curs.rowcount < 1:
            logging.info("No checkins to clusterize.")
            return

        ents_stats = curs.fetchall()
        ents_ids = list(map(lambda x: x[0], ents_stats))
        ents_stats_checkins = list(map(lambda x: x[1], ents_stats))

        (clusters, means_corresponding) = cluster(ents_stats_checkins, 10)

        #Form tuples to write in temporary database
        temp = list(zip(ents_ids, clusters, means_corresponding))

        # Create temporary table to store clusters result
        curs.execute("  CREATE TEMPORARY TABLE temp_clusters (\
                            ent_id integer PRIMARY KEY,\
                            mean DOUBLE PRECISION,\
                            cluster_num integer\
                        ) ON COMMIT DROP;\
                     ")
        logging.info("Clusters for checkins created.")
        # Crunch?
        args_str = ','.join(curs.mogrify("(%s,%s,%s)", x).decode("utf-8") for x in temp)
        curs.execute("INSERT INTO temp_clusters (ent_id, cluster_num, mean) VALUES " + args_str)

        curs.execute("  UPDATE entertainments_stats\
                        SET cluster_checkins_type = temp_clusters.cluster_num,\
                            cluster_checkins_mean = temp_clusters.mean\
                        FROM temp_clusters\
                        WHERE entertainments_stats.ent_id = temp_clusters.ent_id;\
        ")

        c.commit()
        logging.info("Clusters for checkins loaded.")